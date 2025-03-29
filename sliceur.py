def sliceur(file, n=10):
    with open(file, 'rb') as f:  
        data = f.read()

    long = len(data)
    nslice = (long + n - 1) // n  

    slices = []
    for i in range(nslice):
        start = i * n
        end = start + n
        segment = data[start:end]

        if len(segment) < n:
            segment += b'\x00' * (n - len(segment))

        slices.append(segment)

    return slices

def pslice(file, n =10):
    slices=sliceur(file,n)
    with open(slices,"wb"):
        for i in range(len(slices)):
            file.write(slices[i])
