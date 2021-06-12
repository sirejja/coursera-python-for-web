import re


def calculate(data, findall):
    matches = findall(r"([abc])([\+-])?=([abc])?([\+-]?\d+)?")
    for v1, s, v2, n in matches:
        if s == '-':
            data[v1] -= data.get(v2, 0) + int(n or 0)
        elif s == '+':
            data[v1] += data.get(v2, 0) + int(n or 0)
        else:
            data[v1] = data.get(v2, 0) + int(n or 0)

    return data


if __name__ == '__main__':
    def findall(pattern):
        return re.findall(pattern, 'loremc-=a+10ipsuma-=adb+=10olorsitameta=-b+1ololob-=c+100fff')

    data = {"a": 1, "b": 2, "c": 3}
    print("Initial dict:", data)
    result_data = calculate(data, findall)
    print("Final dict:", result_data)