from LzwCompressor.LzwCompressor import LzwCompressor as lzw

compressor = lzw(debug=True)
compressor.compress("test.txt", True)
decompressor = lzw(debug=True)
decompressor.uncompress("test.txt.Z")