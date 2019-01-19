
with open("net_logs.txt", 'r') as fd:
    data = fd.read().split()

dat_log = []
for string in data:
    if string[:10] == '4c47555255':
        dat_log.append(string)
i = 1
with open("hex_extracted.txt", "w+") as fd:
    for logs in dat_log:
        fd.write(logs + "\n")
        i += 1
print(i)
