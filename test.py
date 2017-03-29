import sys
import msgpack

packer = msgpack.Packer()
unpacker = msgpack.Unpacker()

binary = packer.pack("abc super")
unpacker.feed(binary)

for obj in unpacker:
    print(obj)
