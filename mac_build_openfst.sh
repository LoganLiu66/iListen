wget https://www.openfst.org/twiki/pub/FST/WebHome/openfst-1.8.3.tar.gz
tar -xzf openfst-1.8.3.tar.gz
cd openfst-1.8.3
./configure --enable-grm --enable-far --enable-ngram-fsts
make
sudo make install
# add to path
export PATH=/usr/local/bin:$PATH
export LD_LIBRARY_PATH=/usr/local/lib:$LD_LIBRARY_PATH
