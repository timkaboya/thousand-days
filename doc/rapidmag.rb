#!  /usr/bin/ruby

require 'haml'
require 'kramdown'

class Doc
  attr_reader :id, :name
  def initialize id, pth
    @id   = id
    @path = pth
    @name = pth.gsub(/\.txt$/, '').gsub(/\W/, ' ')
  end

  def to_html
    File.open @path do |fch|
      # fch.read.split("\n\n").map {|x| %[<p>#{x}</p>]}.join("\n\n")
      @rod  ||= fch.read
      Kramdown::Document.new(@rod).to_html
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
