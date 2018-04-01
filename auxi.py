from hvdm import hvdm

a = 'a'
b = 'b'
dataset = [[a,1],[a,2],[b,1],[b,2]]
classe = [0,0,1,0]

hvdm = hvdm()
hvdm.config(dataset, classe)
h = hvdm.classificar([a,0])

