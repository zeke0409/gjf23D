# gjf23D
Display the [Gaussian](https://www.hulinks.co.jp/software/chem/gaussian) input in 3D.

## Environment

```
Python 3.8.5
pip 21.3.1
```

## Installation
Install this repository.
```
pip install -r requirements.txt
```

## How to use?
```
python test.py file_name
```

## test
```
python test.py  Gaussian/butadiene.gjf
```

## Assumed gjf grammar
Ignore the first five lines.
```





atom
atom first_atom_num first_atom_distance
atom first_atom_num first_atom_distance second_atom_num planar_angle
atom first_atom_num first_atom_distance second_atom_num planar_angle third_atom_num dihedral_angle
...
```
## Why did I make this?
I was frustrated because every gjf I wrote gave me errors during the training.If you are taking the Advanced Chemistry Laboratory course in Industrial Chemistry at Kyoto University, you should try it.
