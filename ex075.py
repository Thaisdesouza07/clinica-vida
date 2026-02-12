num = (int(input('Digite um numero: ')),
      int(input('Digite outro numero: ')),
      int(input('Digite msis um numero: ')),
      int(input('Digite o ultimo numero: ')))

print(f'Voce informou os valores {num}')
print(f'O valor 9 apareceu {num.count(9)} vezes')
if 3 in num:
    print(f'O valor 3 apareceu na {num.index(3)}ª posição')
else:
    print('O Valor 3 nao foi informado em nenhuma posição')
print('Os valores pares digitados foram: ', end=' ')
for n in num:
    if n % 2 == 0:
        print(n, end=' ')
