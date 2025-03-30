end_sequence = b'\x4E' + b'\x45' + b'\x52' + b'\x4D'

def sliceur(data, n):
    long = len(data)
    nslice = (long + n - 1) // n  

    slices = []
    for i in range(nslice):
        start = i * n
        end = start + n
        segment = data[start:end]

        if len(segment) < n:
            padding_required = n - len(segment)
            segment += end_sequence[:min(padding_required, len(end_sequence))]
            if len(segment) <= n:
                # If the segment is still not long enough, fill with zeros
                segment += b'\x00' * (n - len(segment))
                slices.append(segment)
                return slices
            slices.append(segment)
            segment = end_sequence[padding_required:]
            segment += b'\x00' * (n - len(segment))


        slices.append(segment)

    return slices

def pslice(file, n =10):
    slices=sliceur(file,n)
    with open(slices,"wb"):
        for i in range(len(slices)):
            file.write(slices[i])
