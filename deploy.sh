tar --exclude node_modules -zcvf ccxt-trader.tar.gz src/

scp -o StrictHostKeyChecking=no ccxt-trader.tar.gz root@159.65.75.241:/root/
ssh -o StrictHostKeyChecking=no root@159.65.75.241 tar -xvzf ccxt-trader.tar.gz
ssh -o StrictHostKeyChecking=no root@159.65.75.241 'pkill -9 python && source .bashrc && nohup -c bash "python3.7 src/priceNotificationsDriver.py && python3.7 src/PaperTraderDriver.py" >/dev/null 2>&1 &'
ssh -o StrictHostKeyChecking=no root@159.65.75.241 'cd src/DataBaseJS && npm install && npm run start-prod'
rm -rf ccxt-trader.tar.gz
echo 'done'
