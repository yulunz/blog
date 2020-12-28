---
title: "Throughput vs. Latency"
date: 2020-12-28T11:32:37-06:00
draft: false
---

### Definition

Throughput is the amount of work that's done within a time window. Say I read 100 pages of TAOCP per day, then my throughput 
is 100 pages / day. Or say the network transferred 80 bits per second, the throughput will be 80bps.

Latency, on the other hand, is the time spent waiting before the counterparty gives a response. In networking this is usually the round trip time, starting
 from the client sending a request, until the client hears back from the server. In reality we care more about the _distribution_ of latency. For example,
 we would define an SLA metric from a _percentile_ from the ditribution of latency, e.g. we want 99.95% of our clients' requests to be responded within 300ms. 
Moreover, in some cases it's also important to optimize on the tail - we don't want the 0.05% to experience too much latency. Since those requests that take 
the most time are likely the largest requests, and those who send the largest requests might be the largest customers.

### Relationship

#### Trade-off

Sometimes there is a trade off between throughput and latency. For example a firm wants to migrate their data center to a cloud provider. They can open an internet 
connection to the cloud to upload their data bit by bit. Once a data packet is sent, the cloud provider's server immediately writes the payload into their server - 
the latency is very low through the internet. However, say their upload speed is 50MB/s, in a month they can upload about 130Tb of data. Nowadays firms own 
huge amount of data, much more than hundreds of terabytes. In this case, it might be helpful just to send a 1Pb hard drive through mail to the cloud 
provider and have them load the data upon receival. Latency is much higher by mail, but the total amount of data transferred averaged by time is also a much larger number.

Another example is a _flare gun_, which is an old way for military unit to provide a stress signal to allies. Although it's only able to provide a single flare once (low 
throughput), the latency is also very low - the flare travels with the speed of light. Means of communication with higher throughput typically come with higher 
latency, like sending an encrypted message through radio. 

#### Networking

HTTP network requests consist of multiple back and forth packets between the client and server. If the network is slow (high latency), the parties need to wait longer before
 seeing the response, and it would take longer to complete a request, causing a low throughput. Conversely, if the network
 is fast (low latency), the request would be completed quickly, given other elements are working as expected, resulting in a high throughput.

However, the reverse is not necessarily true. If network has low throughput, it could be high latency, but it could be other reasons as well. For example the network can have a low bandwidth. Similarly, if the network has high throughput, it doesn't mean that the latency must be low - it could be all of a sudden a large amount of data is being transferred after a long time of silence.

#### Scalability

Scalability is one of the main concerns when designing a system. There are two ways a system can be scaled, _vertically_ and _horizontally_. Scaling _vertially_ means that we are giving more processing power to each processing unit, decreasing the time it takes to finish a request, and decreasing the latency. Scaling the system _horizontally_
 means that we are giving more processing units to the system but keeping the processing power of each to be the same. This doesn't decrease the latency but it would increase 
 the throughput.


#


_P.S._: I was asked this question during an interview and although the firm seems to ask every candidate the same question IMO it's still
a very good interview question.

It's open ended - the relationship would be different depend on the context, and a good explanation 
is a result of learning from actual work experience. Althought the candidate can search on the internet beforehand on the definitions, figuring out 
the relationship isn't a given answer (at least until this blog post), and the interviewer can still dive into the answer and gain a better 
understanding of the candidate's knowledge.
