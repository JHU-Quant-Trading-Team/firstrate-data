from manage_db.models import DataBundle

crypto = DataBundle(name='crypto',
                    download_link='https://firstratedata.com/datafile/ZpKb77M8hkSKYkSFg8mY-w/12628',
                    update_link='https://firstratedata.com/datafile/ZpKb77M8hkSKYkSFg8mY-w/13790',
                    root_path='/Users/jacobfeitelberg/Desktop/firstrate-data/data/crypto/')

print(crypto.download())