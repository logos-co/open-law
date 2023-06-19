import {ethers} from 'ethers';
import {SiweMessage} from 'siwe';
import MetaMaskSDK from '@metamask/sdk';
import {hexlify} from '@ethersproject/bytes';
import {toUtf8Bytes} from '@ethersproject/strings';

export function initWallet() {
  // current page url
  const domain = window.location.host;
  // protocol, hostname and port number of the URL
  const origin = window.location.origin;
  // connect to ethereum network and sign transactions with Metamask

  async function signInWithEthereum() {
    if (!window.hasOwnProperty('ethereum')) {
      let result = confirm(
        "You don't have needed extension! Do you want to install it?",
      );
      localStorage.setItem('showExtensionAlert', 'false');
      if (result) {
        window.open('https://metamask.io/', '_blank');
      }
      return;
    }
    if (!window.hasOwnProperty('ethereum')) {
      console.error('Required extension not found');
      return;
    }
    const options = {
      injectProvider: false,
      communicationLayerPreference: 'webrtc',
    };
    const MMSDK = new MetaMaskSDK(options);

    const ethereum = MMSDK.getProvider();
    // create siwe message and call backend to get a nonce
    const res1 = await fetch('/nonce', {
      credentials: 'include',
    });
    const text = await res1.text();
    const response = await ethereum.send('eth_requestAccounts', []); // <- this promps user to connect metamask
    const address = ethers.utils.getAddress(response.result[0]);
    const message = new SiweMessage({
      domain: domain,
      address: address,
      statement: 'Sign in with Ethereum to the app.',
      uri: origin,
      version: '1',
      chainId: '1',
      nonce: text,
    });

    const siweSign = async message => {
      try {
        const from = address;
        const msg = message.signMessage();
        const data = typeof msg === 'string' ? toUtf8Bytes(msg) : msg;
        const hex = hexlify(data);
        const sign = await ethereum.request({
          method: 'personal_sign',
          params: [hex, from],
        });
        debugger;
        return sign;
      } catch (err) {
        console.error(err);
      }
    };

    const sign = await siweSign(message);
    message.signature = sign;

    // post message and signature to backend where it will be verified
    const res2 = await fetch(`/verify`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({message, message}),
      credentials: 'include',
      redirect: 'follow',
    });
    if (res2.status == 200) {
      window.location.replace(res2.url);
    } else window.location.reload();
  }

  const connectWalletBtns = document.querySelectorAll('#connectWalletBtn');

  if (connectWalletBtns) {
    connectWalletBtns.forEach(btn =>
      btn.addEventListener('click', () => {
        signInWithEthereum();
      }),
    );
  }
}
