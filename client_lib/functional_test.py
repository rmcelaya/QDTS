import interfaces_pb2, interfaces_pb2_grpc
import grpc
import json
import pickle
from scipy import stats
import numpy as np

ksid1 = "abcdabcdabcdabc1".encode()
ksid2 = "abcdabcdabcdabc2".encode()
ksid3 = "abcdabcdabcdabc3".encode()

N = 20
key_size = 8

key_size_bytes = int(key_size / 8)
results_file_name = "./results/results_" + str(key_size) + "_" + str(N) + ".pkl"


def run():
    host1 = grpc.insecure_channel('10.4.16.115:31942')
    host2 = grpc.insecure_channel('10.4.16.74:31942')
    host3 = grpc.insecure_channel('10.4.16.132:31942')

    client1 = interfaces_pb2_grpc.ApplicationInterfaceStub(host1)
    client2 = interfaces_pb2_grpc.ApplicationInterfaceStub(host2)
    client3 = interfaces_pb2_grpc.ApplicationInterfaceStub(host3)

    qos = interfaces_pb2.QoS(key_chunk_size=key_size_bytes, timeout=100000, ttl=100000, metadata_mimetype="application/json")

    print("Sending open connects")
    response = client1.open_connect \
        (interfaces_pb2.OpenConnectRequest(source="jamon:munich", destination="pate:nuremberg", qos=qos, ksid=ksid1))
    print("Response: \n" + str(response))

    response = client1.open_connect \
        (interfaces_pb2.OpenConnectRequest(source="jamon:munich", destination="pate:salzburg", qos=qos, ksid=ksid3))
    print("Response: \n" + str(response))

    response = client2.open_connect \
        (interfaces_pb2.OpenConnectRequest(source="jamon:munich", destination="pate:nuremberg", qos=qos, ksid=ksid1))
    print("Response: \n" + str(response))

    response = client2.open_connect \
        (interfaces_pb2.OpenConnectRequest(source="jamon:nuremberg", destination="pate:salzburg", qos=qos, ksid=ksid2))
    print("Response: \n" + str(response))

    response = client3.open_connect \
        (interfaces_pb2.OpenConnectRequest(source="jamon:munich", destination="pate:salzburg", qos=qos, ksid=ksid3))
    print("Response: \n" + str(response))

    response = client3.open_connect \
        (interfaces_pb2.OpenConnectRequest(source="jamon:nuremberg", destination="pate:salzburg", qos=qos, ksid=ksid2))
    print("Response: \n" + str(response))

    input("Press enter when all the keys have been exchanged")

    request1 = interfaces_pb2.GetKeyRequest(ksid=ksid1, metadata_size=100)
    request2 = interfaces_pb2.GetKeyRequest(ksid=ksid1, metadata_size=100)
    request3 = interfaces_pb2.GetKeyRequest(ksid=ksid1, metadata_size=100)


    print("Link 1 tests")
    for i in range(N):
        response1 = client1.get_key(request1)
        response2 = client2.get_key(request1)

        if response1.status != 0 or response2.status != 0:
            print("[FAILED][No key available] Test sample " + str(i))
            exit()

        if response1.key_buffer != response2.key_buffer:
            print("[FAILED][Different buffer] Test sample " + str(i))
            exit()


        print("[OK] Test sample " + str(i) + ". Key: " + str(response1.key_buffer))

    print("Link 2 tests")
    for i in range(N):
        response1 = client2.get_key(request2)
        response2 = client3.get_key(request2)

        if response1.status != 0 or response2.status != 0:
            print("[FAILED][No key available] Test sample " + str(i))
            exit()

        if response1.key_buffer != response2.key_buffer:
            print("[FAILED][Different buffer] Test sample " + str(i))
            exit()


        print("[OK] Test sample " + str(i) + ". Key: " + str(response1.key_buffer))

    print("Link 3 tests")
    for i in range(N):
        response1 = client1.get_key(request3)
        response2 = client3.get_key(request3)

        if response1.status != 0 or response2.status != 0:
            print("[FAILED][No key available] Test sample " + str(i))
            exit()

        if response1.key_buffer != response2.key_buffer:
            print("[FAILED][Different buffer] Test sample " + str(i))
            exit()


        print("[OK] Test sample " + str(i) + ". Key: " + str(response1.key_buffer))

    
    print("ALL TESTS OKAY!")

if __name__ == '__main__':
    run()
