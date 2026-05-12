for i in range(4):
    print("Andhika suka bermain bola")
    
# penerapan range(start, end)
for j in range(5,10):
    print("Index ke-",j)
    
print("-----")
# penerapan list dengan perulangan
buah = ["mangga", "pisang", " apel", "durian"]
for b in buah:
    print(b)
    
print("-----")
aktivitas = ["makan", "minum", "tidur","nonton tv"]
for a in aktivitas:
    print("saya suka", a)
    
    
print("-----")
  # penerapan nested looop
for x in range(1,4):
    for y in range(1,4):
        print("nilai x =", x, "nilai y" , y)
        
print("------")
# penerapan while loop
count = 1
while count <=5:
    print("perulangan ke-", count)
    count +=1
    
print("------")
# penerapan break dan continue
for n in range(1,11):
    if n == 7:
        break
    print("nilai n =", n)
    
print("------")
for m in range(1,11):
    if m % 2 == 0:
        continue
    print("nilai m =", m)
    
print("------")
# penerapam else pada perulangan
for p in range(1,6):
    print("nilai p =", p)
else:
    print("perualangan selesai")
    
print("------")
q = 1
while q <=5:
    print("nilai q =", q)
    q +=1
else:
    print("perulangan while selesai")
    
print("------")
# penerapan pass pada perulangan 
for i in range(1,6):
    pass # placeholder, tidak melakukan apa-apa
print("perulangan dengan pass selesai")

print("------")
# penerapan nested loop dengan break
for a in range(1,4):
    for b in range(1,4):
        if b == 2:
            break
        print("nilai a =", a, "nilai b =", b)
        
print("------")
 # penerapan nested loop dengan continue
for c in range(1,4):
    for d in range(1,4):
        if d == 2:
            continue
        print("nilai c =", c, "nilai d =",d)
            