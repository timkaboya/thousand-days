#!  /usr/bin/ruby

require 'haml'
require 'kramdown'
require 'pathname'

class Doc
  attr_reader :id, :name
  def initialize id, pth
    @id   = id
    @path = pth
    @name = pth.gsub(/\.haml$/, '').gsub(/\.txt$/, '')  #.gsub(/\W/, ' ')
  end

  def to_html
    statdir = Pathname.new((ENV['STATIC_DIR'] || '/static/').to_s)
    File.open @path do |fch|
      @rod  ||= fch.read
      if @path =~ /\.txt$/i then
        Kramdown::Document.new(@rod).to_html
      elsif @path =~ /\.haml/i then
        Haml::Engine.new(@rod).render binding
      else
        @rod
      end
    end
  end
end

def rmain args
  hm    = args.shift
  @docs = File.open(args.shift) {|f| f.read.split("\n")}.map.with_index do |arg, ix|
    Doc.new(ix, arg)
  end
  doc = File.open(hm) do |fch|
    Haml::Engine.new(fch.read)
  end
  $stdout.puts(doc.render(binding))
  0
end

exit(rmain(ARGV))
