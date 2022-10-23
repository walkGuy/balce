# Balce

A chemical formulas parser and balancer in python.

# Get it

`pip install balce`

# Use it

## in command line

`python -m balce`

then you can enter your chemical formulas.

## in python code

```
import balce
fla = balce.CEquation('H2 +O2 = H2O')
bal_fla = fla.balance()
print(fla)
print(bal_fla)
```

Output:

```
H₂+ O₂ = H₂O
2H₂+ O₂ = 2H₂O
```

# Why is it

## The most powerful parser (may be)

It can parse any currently like `(NH3)3[(PO)4·12MoO3·2NH3]5·3H2O^(4+)↑(gas)`



## The most powerful balancer (might be)
