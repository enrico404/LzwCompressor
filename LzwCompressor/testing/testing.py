from LzwCompressor.LzwCompressor import LzwCompressor as lzw

compressor = lzw(debug=True)
compressor.compress("test.flac", True)
decompressor = lzw(debug=True)
decompressor.uncompress("test.flac.Z")