import requests
import h5py
import matplotlib.pyplot as plt

baseurl = 'http://www.illustris-project.org/api/'

headers = {"api-key":"16f22129662d834710bc1f45317d59d0"}


def get(path, params=None):

    r = requests.get(path, params=params, headers=headers)
    r.raise_for_status()

    if r.headers['content-type'] == 'application/json':
        return r.json()
    

    if 'content-disposition' in r.headers:
        filename = r.headers['content-disposition'].split("filename=")[1]
        with open(filename, 'wb') as f:
            f.write(r.content)
        return filename
    
    return r


r = get(baseurl)

sim = get(r['simulations'][4]['url'])

snapshots = get(sim['snapshots'])

last_snap = get( snapshots[-1]['url'])

subhalos_by_mass = get(last_snap['subhalos'], {'limit':10, 'order_by':'-mass_stars'})

#print([subhalos_by_mass['results'][i]['id'] for i in range(5)])

most_massive_subhalo = get( subhalos_by_mass['results'][0]['url'])


individual_subhalo = get(subhalos_by_mass['results'][1]['url'])

mpb1 = get(individual_subhalo['trees']['sublink_mpb'])
f = h5py.File(mpb1, 'r')
f.close()
mpb2 = get(individual_subhalo['trees']['lhalotree_mpb'])

with h5py.File(mpb2, 'r') as f:
    pos = f['SubhaloPos'][:]
    snapnum = f['SnapNum'][:]


for i in range(3):
    plt.plot(snapnum,pos[:,i] - pos[0,i], label=['x', 'y', 'z'][i])

plt.legend()
plt.xlabel('Snapshot Number')
plt.ylabel('Pos$_{x,y,z}$(z) - Pos(z=0)')
plt.show()
