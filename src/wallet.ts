import {ethers} from 'ethers';
import {SiweMessage} from 'siwe';

interface IEthereumOwner extends Window {
  ethereum:
    | ethers.providers.ExternalProvider
    | ethers.providers.JsonRpcFetchFunc;
}

export function initWallet() {
  // current page url
  const domain = window.location.host;
  // protocol, hostname and port number of the URL
  const origin = window.location.origin;
  // connect to ethereum network and sign transactions with Metamask
  const showExtensionAlert = localStorage.getItem('showExtensionAlert');
  if (!window.hasOwnProperty('ethereum') && showExtensionAlert != 'false') {
    let result = confirm(
      "You don't have needed extension! Do you want to install it?",
    );
    localStorage.setItem('showExtensionAlert', 'false');
    if (result) {
      window.open('https://metamask.io/', '_blank');
    }
    return;
  }
  if (showExtensionAlert == 'false' && !window.hasOwnProperty('ethereum')) {
    console.error('Required extension not found');
    return;
  }
  const eOwner: IEthereumOwner = window as any;
  const provider = new ethers.providers.Web3Provider(eOwner.ethereum);
  const signer = provider.getSigner();

  async function signInWithEthereum() {
    // create siwe message and call backend to get a nonce
    const res1 = await fetch('/nonce', {
      credentials: 'include',
    });
    await provider.send('eth_requestAccounts', []); // <- this promps user to connect metamask
    const message = new SiweMessage({
      domain: domain,
      address: await signer.getAddress(),
      statement: 'Sign in with Ethereum to the app.',
      uri: origin,
      version: '1',
      chainId: '1',
      nonce: await res1.text(),
    });
    const signature = await signer.signMessage(message.signMessage());
    message.signature = signature;

    // post message and signature to backend where it will be verified
    const res2 = await fetch(`/verify`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({message, signature}),
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
