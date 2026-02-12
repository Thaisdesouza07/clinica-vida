times = ('Corinthians', 'Palmeiras', 'Santos', 'Grêmio',
         'Cruzeiro', 'Flamengo', 'Vasco', 'Chapecoense',
         'Atlético', 'Botafogo', 'Athletico-PR', 'Bahia',
         'São Paulo', 'Fluminense', 'Sport Recife',
         'EC Vitória', 'Coritiba', 'Avaí', 'Ponte Preta',
         'Atlético-GO')
print('_' * 30)
print(f'Lista de times: {times}')
print('_' * 30)
print(f'Os 5 primeiros são {times[0:6]}')
print('_' * 30)
print(f'Os 4 ultimos são {times[-4:]}')
print('_' * 30)
print(f'Os times em ordem alfabética é {sorted(times)}')
print('_' * 30)
print(f'o Chapecoense esta na {times.index("Chapecoense") +1}ª posição')