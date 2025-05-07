A = 100
B = 1000

print(probe_state(A))
print(probe_state(B))

print(probe_state((float)(A)))

A = 10000

print(probe_state((A)))  # 해시 다를 수 있음
print(probe_state(B))