---
title: "TL; DR: How does HTTPS work?"
date: 2021-06-12T18:44:32-05:00
draft: false
---

On a high level, HTTPS says if you trust a list of organizations that everybody else trusts, it provides an automatic way to extend your trust to any website that is certified by these organizations.

It doesn't say as long as you are using HTTPS, you are safe. Because if you trust the wrong organizations in the first place, whatever website it certifies is not trustworthy as well. Trash in, trash out.

To be more specific, we should first understand what's asymmetric authentication, but even before that, we should start with symmetric authentication. Suppose that Ann and Bob are sending SMS that they don't want others to know about. One way to do this is to share a key beforehand, and the sender will encrypt the message using the *same* key that the receiver will also use to decrypt the message once received. The issue is if they are not careful when sharing this key initially, then a third person like Chris can also talk to Ann using this key, and Ann would have no way to know whether it's Bob or Chris.

Given this, asymmetric authentication uses a pair of keys, a public key, and a private key. If one changes, the other has to change correspondingly. In this case Ann and Bob each keep their own private key, but shares the public key with the other party. When sending a message, the message is encrypted with the private key, but the receiver will decrypt using the sender's public key. So that if Chris knows both their public keys, the maximum he can do is knowing what Ann and Bob are talking about. Chris cannot pretend to be Bob, because Bob's private key is never shared. So when Ann receives a message, with Bob's public key, she always knows this is from the real Bob or not.

As internet's end users, we always want to receive information from the real Bobs. However there are millions and millions of websites, it's not feasible to get millions and millions of public keys, plus Chris's can pretend to be Bob each time a Bob is trying to share a public key. Here we would need a "Certificate Authority", or CA, to help us.

So instead of getting millions and millions of public keys from every website, we instead just need to get public keys from each certificate authority. There are only a small number of commonly used ones. I have about 130 of them on my machine. A certificate authority gives the real website owner a certificate. The certificate includes information like the domain name, expiry date, etc, and the real owner's public key. It also includes a "signature", which is an encryption of these information using the CA's private key. So myself with the CA's public key is able to decrypt the signature and check if the result matches the information above. If so, I know that this CA's has reviewed this website, and I can use the public key in the certificate to decrypt information I received from the website.

If a hacker like Chris forges a certificate himself, he is not going to fill in a valid signature value without the CA's private key. After Ann receives the real certificate and starts to talk with Bob, it is also not possible for Chris to send a bogus message to Ann, because now Ann has the real public key of Bob from the certificate, and Chris doesn't have Bob's private key.

Under this mechanism, which in the internet is referred to as HTTPS, Ann will be able to talk to a lot of real Bobs, and Chris will have very little chance to pretend to be any one of them.

*Some more notes:*

The certificate will expire after a while - currently this will be one year. So that website owners will need to obtain new certificates from the CAs. Otherwise users will see from the browser that "this website's certificate has expired, and it's not safe to continue to view its content". The reason being there might be certain design defects and / or improvements needed in the certificate. Issuing new certificate will help address these issues.

Some website will send a "self-signed" certificate. That is, the signature is produced using it's own private key, instead of the CA's. Self-signed is weaker than a CA-signed certificate, because here, Chris will be able to forge a certificate and have Ann believing that she is talking to Bob. However if Ann already has the real Bob's public key through a real certificate, it's not possible for Chris to pretend to be Bob. User should not trust a website's self-signed certificate.

Digicert is a large commercial CA. However there are more open source friendly CAs like [Let's Encrypt](https://letsencrypt.org/), where you can get certificates and renewals for free.

The certificate is usually the [X.509 certificate](https://en.wikipedia.org/wiki/X.509).
