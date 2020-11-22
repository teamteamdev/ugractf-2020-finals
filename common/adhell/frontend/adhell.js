const BASE_URL = '';

const deleteBanner = function(id) {
    fetch(`${BASE_URL}/api/banners/${id}`, {method: 'DELETE'})
        .then((data) => data.json())
        .then((data) => {
            if (data.status === 'ok') {
                loadCabinet();
            } else {
                alert(data.message);
            }
        });
};

const confirmTransfer = function(id) {
    fetch(`${BASE_URL}/api/transfers/${id}`, {method: 'POST'})
        .then((data) => data.json())
        .then((data) => {
            if (data.status === 'ok') {
                loadCabinet();
            } else {
                alert(data.message);
            }
        });
};

const loadCabinet = function() {
    fetch(`${BASE_URL}/api/me`)
        .then((data) => data.json())
        .then((data) => {
            document.querySelector('#idip').innerHTML = `${data.id} / ${data.ip}`;
            document.querySelector('#name').innerHTML = `${data.name}`;
            document.querySelector('#views').innerHTML = `${data.views}`;
            if (data.views < 1024) {
                document.querySelector('#payout').disabled = true;
            } else {
                document.querySelector('#payout').disabled = false;
            }
            document.querySelector('#balance').innerHTML = `${data.balance}`;

            document.querySelector('#banners').innerHTML = '';

            for (const banner of data.banners) {
                const bannerBlock = document.querySelector('#banner').content.cloneNode(true);
                bannerBlock.querySelectorAll('td')[0].innerHTML = `${banner.name}`;
                bannerBlock.querySelectorAll('td')[1].innerHTML = `${banner.format}`;
                bannerBlock.querySelector('td pre').innerText = `${banner.content}`;
                bannerBlock.querySelector('button').addEventListener('click', () => deleteBanner(banner.id));
                document.querySelector('#banners').appendChild(bannerBlock);
            }

            document.querySelector('#transfers').innerHTML = '';

            for (const transfer of data.incoming_transfers) {
                const transferBlock = document.querySelector('#transfer').content.cloneNode(true);
                transferBlock.querySelectorAll('td')[0].innerHTML = `${transfer.sender}`;
                transferBlock.querySelectorAll('td')[1].innerHTML = `${transfer.amount}`;
                transferBlock.querySelector('button').addEventListener('click', () => confirmTransfer(transfer.id));
                document.querySelector('#transfers').appendChild(transferBlock);
            }
        })
        .catch((err) => alert('Network Error!' + err));
};

const payout = function() {
    fetch(`${BASE_URL}/api/payout`, {method: 'POST'})
        .then((data) => data.json())
        .then((data) => {
            if (data.status === 'ok') {
                loadCabinet();
            } else {
                alert(data.message);
            }
        });
};

const addBanner = function() {
    fetch(`${BASE_URL}/api/banners`, {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({
            name: document.querySelector('#bannerName').value,
            format: document.querySelector('#bannerFormat').value,
            content: document.querySelector('#bannerUrl').value
        })
    })
        .then((data) => data.json())
        .then((data) => {
            if (data.status === 'ok') {
                loadCabinet();
            } else {
                alert(data.message);
            }
        });
};

const addTransfer = function() {
    fetch(`${BASE_URL}/api/transfers`, {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({
            receiver_id: parseInt(document.querySelector('#transferTarget').value, 10),
            amount: parseInt(document.querySelector('#transferAmount').value, 10)
        })
    })
        .then((data) => data.json())
        .then((data) => {
            if (data.status === 'ok') {
                loadCabinet();
            } else {
                alert(data.message);
            }
        });
};

window.onload = function() {
    loadCabinet();
    document.querySelector('#update').addEventListener('click', loadCabinet);
    document.querySelector('#payout').addEventListener('click', payout);

    document.querySelector('#bannerAdd').addEventListener('click', addBanner);
    document.querySelector('#transferAdd').addEventListener('click', addTransfer);
};
