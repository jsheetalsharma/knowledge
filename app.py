
import streamlit as st
from pathlib import Path
import json

st.set_page_config(
    page_title="Backend Interview Prep",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded",
)

DATA = {
"Java": {
"priority": "P0",
"sections": {
"HashMap — the easy way": """
### What problem does HashMap solve?

Imagine you have a cupboard with many drawers.

Each drawer is a **bucket**. You want to store:

```text
Sheetal → 35
Rahul   → 28
Priya   → 31
```

When you do `map.put("Sheetal", 35)`, Java uses `"Sheetal".hashCode()` to decide **which drawer** to use.

```text
"Sheetal"
    ↓
hashCode()
    ↓
bucket number
    ↓
store Sheetal → 35
```

When you call `map.get("Sheetal")`, Java calculates the hash again and goes to that bucket directly.

That is why HashMap lookup is **usually O(1)**.

### What is a collision?

Two different keys can land in the same bucket:

```text
"Sheetal" → Bucket 4
"Rahul"   → Bucket 4
```

That's a **collision**.

The bucket can hold multiple entries. In modern Java, heavily-colliding buckets can be converted from a linked structure into a balanced tree when implementation thresholds are met.

### Where does equals() come in?

`hashCode()` tells HashMap **WHERE to look**.

`equals()` tells it **WHICH key** it has found.

So remember:

> **hashCode → WHERE**  
> **equals → WHICH**

### Why must equals() and hashCode() agree?

If:

```java
a.equals(b) == true
```

then:

```java
a.hashCode() == b.hashCode()
```

must also be true.

Otherwise equal keys can be sent to different buckets.

### The mutable-key trap

Suppose an object is a key and its `hashCode()` depends on `name`.

```text
Person("A") → Bucket 2
```

You put it into the map and then change the name:

```text
Person("B") → Bucket 7
```

The entry is still sitting where it was originally stored, but future lookups use the new hash. The entry can become effectively unreachable.

**Interview rule:** use immutable keys, or never mutate fields used by `equals()`/`hashCode()` while the object is a key.

### Interview answer

> HashMap uses an array of buckets. The key's hashCode is used to find a bucket, and equals is used to identify the exact key inside that bucket. Average lookup is O(1). Collisions are handled inside a bucket, and heavily-colliding buckets can become trees in modern Java. Keys should obey the equals/hashCode contract and should generally be immutable.
""",
"Collections": """
### ArrayList vs LinkedList

Think of `ArrayList` as numbered seats in a row:

```text
0   1   2   3   4
A   B   C   D   E
```

Finding item 3 is fast: **O(1)**.

`LinkedList` is more like people holding hands:

```text
A → B → C → D → E
```

To reach D, you walk through A → B → C. Indexed access is O(n).

**Practical rule:** ArrayList is the default choice in most application code because it has excellent cache locality and fast indexed access.

### HashSet

A Set means:

> "I only care whether this thing exists; duplicates are not allowed."

HashSet uses hashing underneath, so `hashCode()` and `equals()` determine uniqueness.

### ConcurrentHashMap

A normal HashMap is not safe for concurrent mutation.

ConcurrentHashMap is designed for multiple threads accessing/updating a shared map without one giant lock around the entire structure.

Use it when you genuinely have shared mutable map state across threads.

### Queue vs Deque

A Queue usually means:

```text
producer → [A][B][C] → consumer
```

A Deque allows adding/removing from both ends.

For most interview answers, first identify the access pattern, then choose the collection.
""",
"Generics": """
### Why do we use generics?

Without generics:

```java
List list = new ArrayList();
list.add("hello");
list.add(10);
```

Now the list can contain unrelated types.

With generics:

```java
List<String> names = new ArrayList<>();
```

The compiler protects you from putting the wrong type in.

### `? extends` vs `? super`

A simple memory trick:

- `? extends T` → you **read** T-like values safely.
- `? super T` → you can **write** T values safely.

Example:

```java
List<? extends Number> numbers
```

You can safely read Numbers.

```java
List<? super Integer> numbers
```

You can safely add Integers.

The classic mnemonic is **PECS: Producer Extends, Consumer Super**.
"""
}},
"Java Concurrency": {
"priority": "P0",
"sections": {
"Threads, race conditions and locks": """
### What is a race condition?

Imagine two people update the same bank balance at the same time.

Balance = 100.

Both read 100.

Both add 50.

Both write 150.

Expected: 200.

Actual: 150.

That's a race condition.

The key question is:

> **What shared state must remain correct?**

Then choose a synchronization strategy.

### synchronized

`synchronized` says:

> "Only one thread at a time can enter this protected section."

It is simple and automatically releases the monitor when leaving the block/method.

### Lock

`Lock` gives more control: `tryLock()`, interruptible acquisition, and explicit lock management.

If simple mutual exclusion is enough, `synchronized` is often easier and safer.

### volatile

`volatile` mainly gives **visibility** and ordering guarantees.

It does NOT make:

```java
count++;
```

atomic.

That operation is really:

```text
read
add
write
```

Another thread can interfere between those steps.
""",
"AtomicInteger and LongAdder": """
`AtomicInteger` uses atomic CPU-level operations such as CAS.

Good when you need atomic updates to one value.

`LongAdder` spreads updates across multiple internal cells. Under very high contention, this can reduce fighting between threads.

Easy picture:

```text
AtomicInteger:
Thread A ─┐
Thread B ─┼→ one counter ← Thread C
Thread D ─┘

LongAdder:
Thread A → cell 1
Thread B → cell 2
Thread C → cell 3
Thread D → cell 4
             ↓
           total
```

Use the simplest primitive that matches the requirement.
""",
"ExecutorService": """
Creating a new thread for every task is like hiring a new employee for every email.

Instead, keep a team of workers:

```text
Tasks → [Thread Pool]
          ├─ Worker 1
          ├─ Worker 2
          └─ Worker 3
```

`ExecutorService` manages those workers.

A production system should usually have:
- bounded concurrency
- sensible queue size
- clear shutdown behavior
- metrics for queue depth and task duration
- separate pools for workloads with different failure characteristics

An unbounded queue can hide overload until the service runs out of memory or latency becomes terrible.
""",
"CompletableFuture": """
Think of `CompletableFuture` as saying:

> "Start this work, and when it finishes, do the next thing."

Good:

```text
call A
  ↓
when A finishes
  ↓
call B
  ↓
combine result
```

Common mistakes:
- blocking with `.get()` everywhere
- accidentally using the common pool for blocking work
- no timeout
- swallowing exceptions
- unbounded fan-out

For blocking I/O, use an executor designed for that workload.
""",
"Deadlock": """
A deadlock is two or more threads waiting forever for each other.

```text
Thread A owns Lock 1 → waits for Lock 2
Thread B owns Lock 2 → waits for Lock 1
```

Nobody can move.

Prevent it by:
- consistent lock ordering
- short critical sections
- avoiding nested locks where possible
- `tryLock()` with timeout when appropriate
- reducing shared mutable state
- using message passing/immutable designs
"""
}},
"JVM & Performance": {
"priority": "P0",
"sections": {
"Heap, Stack and Metaspace": """
A simple mental model:

```text
Thread
  ↓
Stack → current method calls / local execution state

JVM
  ↓
Heap → objects and application data

JVM
  ↓
Metaspace → class metadata
```

Don't overstate the physical placement of every variable/object—the JVM can optimize aggressively.

### GC

Garbage collection finds objects that are no longer reachable and reclaims memory.

For interview purposes, focus on:
- allocation rate
- live-set size
- pause time
- throughput
- selected GC collector
- CPU cost

Avoid memorizing old GC terminology without understanding what problem it solves.
""",
"Debug high CPU": """
Use evidence, not guesses.

1. Confirm CPU is actually high.
2. Identify the affected instance/pod.
3. Find hot threads using thread dumps/profiling.
4. Inspect stack traces.
5. Correlate with request rate, deployments, GC and lock contention.
6. Reproduce if possible.
7. Fix the hotspot.
8. Add a regression test/metric.

A Lead answer should say **how you would prove the cause**.
""",
"Debug memory growth": """
First ask:

> Is memory growing because the workload legitimately grew, or because objects are being retained unexpectedly?

Check:
- heap after GC
- allocation rate
- GC behavior
- heap dump
- retained-object paths
- caches without eviction
- unbounded collections
- ThreadLocal misuse
- listeners/callbacks
- large payload retention

Don't immediately increase the heap. That can hide the problem.
"""
}},
"Spring Boot": {
"priority": "P0",
"sections": {
"Dependency Injection": """
Spring creates objects called **beans** and connects their dependencies.

Instead of:

```java
Service service = new Service(new Repository());
```

Spring can build the object graph for you.

Prefer constructor injection:

```java
class Service {
    private final Repository repository;

    Service(Repository repository) {
        this.repository = repository;
    }
}
```

Why?
- dependency is explicit
- field can be final
- easy unit testing
- fails early if dependency is missing
""",
"@Transactional": """
Think of a transaction as a box:

```text
BEGIN
  change A
  change B
  change C
COMMIT
```

If something goes wrong:

```text
ROLLBACK
```

Spring commonly applies transaction behavior through a proxy.

Important trap:

```java
this.otherTransactionalMethod();
```

A self-invocation can bypass the proxy, so the expected transactional behavior may not be applied.

### REQUIRED vs REQUIRES_NEW

`REQUIRED`:
- join existing transaction
- otherwise create one

`REQUIRES_NEW`:
- suspend existing transaction
- create a completely separate transaction

REQUIRES_NEW is useful for independent audit/outbox work, but too much nesting can exhaust DB connections.
""",
"Isolation levels": """
Imagine two people editing the same spreadsheet.

Isolation controls **how much one transaction can see from another transaction**.

From weakest to strongest conceptually:

```text
Read Uncommitted
Read Committed
Repeatable Read
Serializable
```

Higher isolation can reduce concurrency.

Don't answer with "always use Serializable."

Instead say:

> "I choose isolation based on the business invariant and database behavior."
""",
"REST error handling": """
A production API should return a predictable error shape.

For example:

```json
{
  "code": "INVALID_ACCOUNT",
  "message": "The account is invalid",
  "traceId": "abc123"
}
```

Use centralized exception handling such as `@RestControllerAdvice`.

Never expose stack traces, SQL details or internal implementation details to clients.
""",
"Production-ready Spring service": """
Think beyond "it works on my laptop."

A production service needs:
- timeouts
- connection-pool limits
- graceful shutdown
- readiness/liveness probes
- logs, metrics and traces
- secure configuration
- validation
- idempotency where needed
- bounded concurrency
- safe rollout/rollback
- meaningful tests
"""
}},
"Kafka": {
"priority": "P0",
"sections": {
"Kafka in one picture": """
Kafka is easiest to understand as a **durable distributed log**.

```text
Producers
   ↓
 Topic
 ├── Partition 0
 ├── Partition 1
 └── Partition 2
        ↓
   Consumer Group
 ┌─────────────┐
 │ Consumer A  │ → P0
 │ Consumer B  │ → P1
 │ Consumer C  │ → P2
 └─────────────┘
```

A topic is split into partitions.

A consumer group shares the work: each partition is owned by one consumer in that group at a time.

### Most important rule

> **Kafka ordering is guaranteed within a partition, not across the entire topic.**
""",
"Partition key": """
Suppose account events must stay in order:

```text
account-123:
deposit
withdrawal
balance-update
```

Use `accountId` as the key.

Kafka hashes the key and sends those records to the same partition.

The trade-off is important:

> If one key becomes extremely hot, that partition can become a bottleneck.

If strict ordering is not required, you can shard the hot key. If strict ordering is required, you must preserve the smallest necessary ordering scope.
""",
"Consumer groups and rebalancing": """
A consumer group divides partitions among consumers.

If a consumer dies:

```text
Before:
Consumer A → P0
Consumer B → P1
Consumer C → P2

C dies

After:
Consumer A → P0
Consumer B → P1 + P2
```

This reassignment is a **rebalance**.

Frequent rebalances hurt throughput and latency.

Investigate:
- long processing
- poll settings
- unstable consumers
- deployment churn
- slow dependencies
""",
"Delivery semantics": """
Three useful concepts:

**At-most-once**
```text
process once → may lose data
```

**At-least-once**
```text
don't lose easily → duplicates possible
```

**Exactly-once**
```text
a carefully scoped processing guarantee
```

The trap:

> Exactly-once Kafka processing does NOT magically make an arbitrary external database/API side effect exactly-once.

For external effects, use idempotency, transactions where supported, or an outbox/inbox pattern.
""",
"Retries and poison messages": """
A retry is useful when failure is temporary.

Bad:

```text
failure → retry → failure → retry → retry forever
```

This can make an outage worse.

Better:

```text
temporary failure
      ↓
bounded retry + exponential backoff + jitter
      ↓
still failing?
      ↓
DLQ / quarantine
```

A poison message is one that keeps failing because of a permanent problem. Don't let it block the entire pipeline forever.
""",
"Kafka lag": """
Lag simply means:

> "Producers have produced more data than consumers have processed."

To diagnose it:

1. Did producer traffic increase?
2. Did consumer throughput drop?
3. Is one partition hot?
4. Is a downstream DB/API slow?
5. Are consumers constantly rebalancing?
6. Is the processing logic now more expensive?

Only then decide whether scaling consumers will help.

More consumers cannot create useful parallelism beyond the number of partitions.
""",
"Outbox pattern": """
Classic failure:

```text
DB transaction succeeds
        ↓
service crashes
        ↓
Kafka publish never happens
```

Now the database says the operation happened, but nobody received the event.

Outbox fixes this:

```text
One DB transaction
 ├─ business data
 └─ outbox event

        ↓

publisher reads outbox
        ↓
Kafka
```

The database change and outbox record commit together.

Consumers should still be idempotent because the publisher/consumer path can retry.
"""
}},
"Stream Processing / Flink Concepts": {
"priority": "P0",
"sections": {
"Why stream processing?": """
Batch processing says:

> "Collect data, then process it."

Stream processing says:

> "Process data as it arrives."

For example:

```text
Event → validate → enrich → aggregate → result
  ↑
happens continuously
```

Flink is designed for distributed, stateful stream processing.
""",
"Processing time vs event time": """
Suppose an event happened at 10:00 but the network delayed it until 10:05.

**Processing time** = 10:05

**Event time** = 10:00

If the business question is "what happened between 10:00 and 10:01?", event time is what you want.

This is why event-time processing matters when data arrives late or out of order.
""",
"Watermarks": """
A watermark is basically the system saying:

> "I believe we have seen events up to approximately this event-time point."

Example:

```text
Events:
10:00
10:02
10:01  ← arrived late

watermark ≈ 10:02
```

Watermarks let windows decide when enough time has passed to produce results while still allowing some out-of-order events.
""",
"Keyed state": """
Suppose you want a running total for every customer.

```text
Customer A → 100
Customer B → 250
Customer C → 80
```

That is state associated with a key.

Flink can partition that state across parallel workers.

The important design questions are:
- how large can state become?
- how is it checkpointed?
- what happens when a worker fails?
- how do keys distribute across workers?
""",
"Checkpoints and recovery": """
A checkpoint is like saving a game.

```text
running job
    ↓
checkpoint
    ↓
more processing
    ↓
CRASH!
    ↓
restore checkpoint
    ↓
continue
```

The checkpoint contains consistent state needed for recovery.

Checkpoint frequency is a trade-off:
- too frequent → overhead
- too infrequent → more work to replay after failure
""",
"Exactly-once in stream processing": """
Exactly-once is not a magic word.

It means the processing framework can ensure a carefully defined result is not duplicated during recovery, assuming the source/sink participate correctly.

For an external database:

```text
Flink exactly-once
       ≠
arbitrary DB side effect exactly-once
```

The sink must support transactions or idempotent writes if you need end-to-end correctness.
""",
"Backpressure": """
Imagine a factory:

```text
Machine A → Machine B → Machine C
100 items/s    50 items/s
```

Machine B cannot keep up.

The queue grows.

In stream processing this is **backpressure**.

You find the slow operator/sink and fix the bottleneck rather than simply increasing every worker.
""",
"Late events": """
Real-world events do not always arrive in order.

Possible strategy:
- event-time windows
- watermark
- allowed lateness
- side output for very late events
- correction/retraction if results need updating

Always define the business rule:

> "How late is acceptable, and what should happen after that?"
"""
}},
"AWS & Kubernetes": {
"priority": "P0",
"sections": {
"EKS mental model": """
Think of Kubernetes as a manager of containers.

```text
Kubernetes
   ↓
Pods
   ↓
Containers
```

EKS provides the managed Kubernetes control plane; your workloads still need good configuration for:
- resources
- networking
- IAM
- scaling
- deployment
- observability
- security
""",
"Readiness vs liveness": """
**Readiness** asks:

> "Should this pod receive traffic?"

**Liveness** asks:

> "Is this process so broken that it should be restarted?"

Important production lesson:

If a database is temporarily down, you often do NOT want every pod to fail its liveness probe and restart repeatedly.

That can create a restart storm.

Readiness can remove the pod from traffic while keeping the process alive.
""",
"Scaling": """
Horizontal scaling:

```text
2 pods → 5 pods
```

Vertical scaling:

```text
2 CPU → 4 CPU
```

HPA can scale pods from CPU/memory or custom metrics.

For Kafka consumers, **consumer lag** may be a much better scaling signal than CPU.

For stream processing, throughput/backpressure/operator utilization can be more meaningful.
""",
"Safe deployment": """
A good deployment pipeline looks like:

```text
code
 ↓
tests
 ↓
security scans
 ↓
immutable artifact
 ↓
controlled deployment
 ↓
health checks
 ↓
canary/progressive rollout
 ↓
metrics
 ↓
continue OR rollback
```

A Lead should talk about rollback, not just deployment.
""",
"Security basics": """
Use:
- least-privilege IAM
- workload identity
- TLS
- encryption at rest
- secrets manager
- network controls
- image/dependency scanning
- audit logs
- controlled access

Never put secrets into source code, container images or normal logs.
"""
}},
"Distributed Systems": {
"priority": "P0",
"sections": {
"Timeouts, retries and circuit breakers": """
Think about a service calling another service.

Without a timeout:

```text
Service A waits
Service A waits
Service A waits
...
threads get stuck
```

A timeout says:

> "I won't wait forever."

Retry says:

> "This might be temporary; try again."

Circuit breaker says:

> "This dependency is clearly unhealthy; stop calling it for a while."

These work together, but retries must be bounded and use backoff + jitter.
""",
"Why retries can be dangerous": """
Imagine a dependency can handle 1,000 requests/sec.

It becomes unhealthy.

Instead of 1,000 requests, 1,000 callers each retry 3 times.

Now the dependency gets hit with thousands more requests exactly while it is sick.

This is a **retry storm**.

Use:
- retryable-error classification
- bounded attempts
- exponential backoff
- jitter
- retry budgets
- idempotency
""",
"Bulkheads": """
A bulkhead prevents one workload from consuming everything.

Imagine a ship:

```text
| compartment A | compartment B |
```

If A floods, B survives.

In software:
- separate thread pools
- separate connection pools
- concurrency limits
- separate queues

This limits blast radius.
""",
"Idempotency": """
Idempotency means:

> Repeating the same logical operation produces the same logical outcome.

Example:

```text
POST /payment
Idempotency-Key: abc123
```

If the client times out and sends the same request again, the server recognizes `abc123` and does not create a second payment.

Store the key and outcome durably enough to survive retries and concurrent duplicates.
""",
"CAP theorem": """
During a network partition, you cannot guarantee both perfect consistency and full availability for every operation.

The useful interview question is:

> "Which business operations absolutely require strong consistency, and where can we tolerate temporary staleness?"

Don't just say "pick two."
""",
"Eventual consistency": """
Suppose one service updates a customer name.

Another service learns about it a little later.

For a short time:

```text
Service A → new name
Service B → old name
```

Eventually they converge.

That's eventual consistency.

It is fine when temporary staleness is acceptable.

For critical invariants, keep the authoritative decision in a strongly consistent boundary.
"""
}},
"System Design": {
"priority": "P0",
"sections": {
"How to start any system design": """
Do NOT immediately draw boxes.

Use this sequence:

1. Clarify requirements.
2. Estimate traffic and data volume.
3. Define APIs/events.
4. Identify core data.
5. Draw the high-level architecture.
6. Choose storage based on access patterns.
7. Add asynchronous boundaries where useful.
8. Discuss scaling.
9. Discuss failures.
10. Discuss consistency/idempotency.
11. Discuss security.
12. Discuss observability.
13. State trade-offs.

At Lead level, the **failure path** is as important as the happy path.
""",
"Design: Real-time event processing": """
### Problem

Ingest a huge stream of events, process them in real time, maintain state, and expose low-latency results.

### Architecture

```text
Producers
   ↓
Kafka
   ↓
Flink
 ├─ validation
 ├─ enrichment
 ├─ state
 └─ aggregation
   ↓
Serving store ─→ API
   ↓
Data lake for history
```

Add:
- schema compatibility
- partitioning
- checkpoints
- idempotent sinks
- DLQ/quarantine
- replay
- metrics/traces
- autoscaling

### Failure questions

What if one key is hot?

What if Flink crashes?

What if the serving database is slow?

What if events arrive late?

What if an event is processed twice?

Answer each explicitly.
""",
"Design: Notification platform": """
```text
API
 ↓
durable queue
 ↓
routing
 ↓
provider workers
 ├─ email
 ├─ SMS
 └─ push
 ↓
delivery events
```

Important:
- idempotency
- provider rate limits
- retries
- circuit breakers
- DLQ
- user preferences
- templates
- provider failover
- status tracking

Keep slow provider calls out of the synchronous API path.
""",
"Design: Distributed rate limiter": """
First define the rule:

```text
100 requests/minute/user?
100 requests/second/client?
burst allowed?
```

A token bucket is a common choice.

```text
tokens
  ↓
request → take token?
        ↙      ↘
      yes       no
       ↓         ↓
    allow      reject
```

A shared low-latency store such as Redis can hold the state when its consistency/availability trade-offs are acceptable.

Use atomic operations so two servers cannot both believe the last token is available.
""",
"Design: Data ingestion platform": """
```text
Sources
  ↓
Kafka
  ↓
validation/schema checks
  ↓
raw immutable data
  ↓
processing
  ↓
curated data
  ↓
analytics
```

Keep raw data replayable.

That gives you a safety net:

```text
bad transformation
      ↓
fix code
      ↓
replay raw data
      ↓
rebuild curated result
```

Discuss retention, partitioning, schema evolution, data quality, lineage, encryption and access control.
""",
"System design numbers": """
Always estimate.

If a system receives 1 billion events/day:

```text
1,000,000,000 / 86,400
≈ 11,574 events/sec average
```

Then ask:

> "What is peak traffic?"

If peak is 5× average:

```text
≈ 58,000 events/sec
```

This is why a Lead engineer should not size infrastructure from daily averages alone.

Use headroom and define what happens during overload.
"""
}},
"LLD & Code Review": {
"priority": "P1",
"sections": {
"LRU Cache": """
Use two structures:

```text
HashMap → find node quickly
Doubly linked list → track most/least recently used
```

Conceptually:

```text
Map
 A → Node A
 B → Node B

List:
MRU → A → C → B → LRU
```

On access:
- find node in O(1)
- move it to front in O(1)

When full:
- remove tail
- remove that key from map

Target: O(1) get and O(1) put.
""",
"Producer-consumer": """
The easiest production answer is usually `BlockingQueue`.

```text
Producer
   ↓
BlockingQueue
   ↓
Consumer
```

The queue provides coordination.

If implementing manually, you must define:
- capacity
- blocking behavior
- shutdown
- interruption
- concurrency correctness
- fairness expectations
""",
"Retry utility": """
A good retry utility should have:

```text
max attempts
retryable error predicate
backoff
jitter
deadline/timeout
metrics
```

It should NOT blindly retry everything.

The operation should also be idempotent or otherwise safe to repeat.
""",
"Code review checklist": """
When reading unfamiliar production code, scan in this order:

1. Correctness
2. Concurrency
3. Transaction boundaries
4. Error handling
5. Security
6. Performance
7. Maintainability
8. Testability
9. Observability

Look for:
- unbounded queues
- no timeouts
- broad exception swallowing
- N+1 queries
- transaction mistakes
- sensitive logs
- hidden shared state
- missing tests
"""
}},
"Testing & Production": {
"priority": "P1",
"sections": {
"Testing pyramid": """
Different tests answer different questions.

```text
        E2E
       /   \
 integration
     /       \
   unit tests
```

Unit tests are fast and numerous.

Integration tests verify real boundaries such as Kafka/database behavior.

Contract tests catch incompatible API/event changes.

End-to-end tests cover critical business flows but are slower and more fragile.
""",
"Streaming test strategy": """
For a streaming system, test:
- transformation logic
- event ordering
- duplicate events
- late events
- schema evolution
- checkpoint/recovery behavior
- sink failures
- high throughput
- backpressure
- replay correctness

A particularly valuable test is:

> "If I replay the same input after a failure, do I get the correct final state?"
""",
"Production incident": """
A strong incident response:

```text
1. Stabilize
2. Reduce blast radius
3. Communicate
4. Diagnose
5. Recover
6. Verify
7. RCA
8. Prevent recurrence
```

Don't start by hunting for someone to blame.

Find the system condition that allowed the failure.
""",
"Observability": """
Logs tell you **what happened**.

Metrics tell you **how much/how often**.

Traces tell you **where time went across services**.

For streaming systems also monitor:
- consumer lag
- throughput
- processing latency
- checkpoint duration/failures
- backpressure
- state size
- DLQ rate
- late events
- queue age
"""
}},
"Security & AI-assisted Engineering": {
"priority": "P1",
"sections": {
"REST API security": """
Think:

```text
Who are you?        → Authentication
What can you do?    → Authorization
Can I trust input?  → Validation
Can traffic abuse?  → Rate limiting
Can secrets leak?   → Secure logging/config
Can we investigate? → Audit trail
```

Also use TLS, secure dependencies, least privilege and appropriate encryption.
""",
"AI-assisted engineering": """
AI-generated code should be treated as **untrusted input**.

A safe engineering workflow is:

```text
AI suggestion
    ↓
human review
    ↓
compile/tests
    ↓
security scan
    ↓
architecture review
    ↓
production approval
```

Never let AI bypass normal engineering controls.

For enterprise use, also think about:
- approved tools
- sensitive-data boundaries
- secrets
- intellectual property
- licensing
- auditability
- measurable outcomes
""",
"Good answer to an AI leadership question": """
> "I would start with approved enterprise tools and low-risk use cases such as scaffolding, test generation, refactoring, documentation and code-review assistance. I would define guardrails for sensitive data, secrets, licensing, security and human review. Then I would measure cycle time, review effort, escaped defects and developer productivity rather than simply measuring AI usage."
"""
}},
"Leadership & Behavioral": {
"priority": "P0",
"sections": {
"How to answer leadership questions": """
Use STAR:

```text
S — Situation
T — Task
A — Action
R — Result
```

But for a Lead role, add:

> "What did I learn and what changed afterward?"

Avoid spending two minutes explaining background before getting to what **you** did.
""",
"Six stories to prepare": """
Prepare one story for each:

1. Major technical decision
2. Production incident
3. Conflict/disagreement
4. Mentoring someone
5. Delivery under pressure
6. A decision that went wrong

Each story should contain:
- your ownership
- alternatives considered
- decision
- measurable result
- lesson
""",
"Influence without authority": """
A strong answer:

> "I start by understanding the other person's goal. Then I make the decision criteria explicit, use data/prototypes/design docs where useful, and look for a small experiment that can settle disagreement. If there is still disagreement, I escalate the decision with the trade-offs clearly documented."

The key is not "I convinced everyone."

The key is **how you created a good decision**.
""",
"Technical debt": """
Don't say:

> "We should clean up the code."

Say:

> "This debt causes X incidents/month, adds Y minutes to deployments, creates Z security risk, or blocks feature delivery. Therefore I would prioritize it against business work."

Connect technical debt to business impact.
""",
"Mentoring": """
A Lead doesn't just give answers.

A good mentoring loop is:

```text
understand current level
        ↓
ask questions
        ↓
give direction
        ↓
let person attempt
        ↓
review
        ↓
increase ownership
```

The goal is to make the person less dependent on you over time.
"""
}},
"Rapid Fire": {
"priority": "P1",
"sections": {
"Questions": """
Practice answering these aloud in 30–60 seconds each:

1. Why does ConcurrentHashMap disallow null?
2. What happens during Kafka consumer rebalance?
3. Why is Kafka ordering only within a partition?
4. What causes consumer lag?
5. What is a poison message?
6. What is a tombstone record?
7. What is schema evolution?
8. What happens when a Flink worker dies?
9. Why do watermarks matter?
10. What causes backpressure?
11. What is keyed state?
12. What is a checkpoint?
13. Why can retries cause an outage?
14. What is a circuit breaker?
15. What is a bulkhead?
16. How do you make a POST idempotent?
17. What is eventual consistency?
18. When do you need strong consistency?
19. What is an outbox?
20. Why can DB connection pools become bottlenecks?
21. Readiness vs liveness?
22. What causes an OOMKill?
23. How do you debug high CPU?
24. How do you debug p99 latency?
25. What is a cache stampede?
26. When would you not use Redis?
27. How do you safely deploy a risky change?
28. What should never go into logs?
29. How do you test a streaming pipeline?
30. How do you evaluate AI-generated code?
"""
}},
"Revision Plan": {
"priority": "P0",
"sections": {
"Limited-time plan": """
### If you have several study blocks

**Day 1**
- Java concurrency
- HashMap/collections
- Kafka fundamentals
- Speak one system design aloud

**Day 2**
- Flink
- Spring transactions
- Kafka failure scenarios
- Speak a second system design aloud

**Day 3**
- AWS/Kubernetes
- distributed systems
- production incidents
- behavioral stories
- project architecture deep dive

**Interview day**
- No major new topic
- Review cheat sheet
- Rapid-fire answers
- Review your 6 leadership stories
- Review 2 project architectures

### If you only have 3 hours

60 min → Java concurrency + Spring

45 min → Kafka

35 min → Flink

25 min → system design

15 min → AWS/EKS

40 min → leadership + project stories

The goal is not to know everything. The goal is to explain the important things clearly.
""",
"Final cheat sheet": """
### When asked about Kafka

```text
partition key
→ ordering
→ replication
→ consumer groups
→ lag
→ retries/DLQ
→ idempotency
→ observability
```

### When asked about stream processing

```text
event time
→ watermarks
→ keyed state
→ checkpoints
→ recovery
→ backpressure
→ sink semantics
```

### When asked system design

```text
requirements
→ scale
→ APIs/events
→ data
→ architecture
→ consistency
→ failure
→ security
→ observability
→ trade-offs
```

### When asked a leadership question

```text
context
→ your ownership
→ decision
→ influence
→ result
→ lesson
```
"""
}}
}

# Flatten
def get_all_topics():
    result=[]
    for cat, val in DATA.items():
        for sec in val["sections"]:
            result.append((cat, sec, val["priority"]))
    return result

topics = get_all_topics()

# Session state
if "done" not in st.session_state:
    st.session_state.done = set()

st.sidebar.title("🧠 Interview Prep")
st.sidebar.caption("Technology + system design + leadership")

pages = ["🏠 Dashboard"] + list(DATA.keys())
page = st.sidebar.radio("Go to", pages)

if page == "🏠 Dashboard":
    st.title("Backend Interview Prep")
    st.subheader("Learn the idea first. Then learn the interview answer.")
    st.info("This portal intentionally contains no personal, employer, or interview-company information.")

    total = len(topics)
    done = len(st.session_state.done)
    pct = done / total if total else 0
    st.progress(pct)
    st.metric("Topics completed", f"{done} / {total}")

    st.markdown("### How to use this")
    st.markdown("""
1. Start with **P0** topics.
2. Read the **easy explanation**.
3. Close the page mentally and explain it yourself.
4. Use the interview wording only after the concept is clear.
5. Mark the topic complete.
6. Practice system design aloud instead of only reading it.
""")

    cols = st.columns(3)
    p0 = sum(1 for _,_,p in topics if p=="P0")
    p1 = sum(1 for _,_,p in topics if p=="P1")
    cols[0].metric("P0 topics", p0)
    cols[1].metric("P1 topics", p1)
    cols[2].metric("All topics", total)

    st.markdown("### Recommended order")
    for x in ["Java", "Java Concurrency", "Spring Boot", "Kafka", "Stream Processing / Flink Concepts",
              "Distributed Systems", "System Design", "AWS & Kubernetes", "LLD & Code Review",
              "Testing & Production", "Security & AI-assisted Engineering", "Leadership & Behavioral", "Rapid Fire"]:
        st.markdown(f"- **{x}**")

else:
    category = DATA[page]
    st.title(page)
    st.caption(f"Priority: {category['priority']}")

    search = st.text_input("🔎 Search this section", placeholder="e.g. transaction, retry, watermark...")
    sections = category["sections"]

    for name, content in sections.items():
        if search and search.lower() not in (name + " " + content).lower():
            continue
        key = f"{page}::{name}"
        with st.expander(("✅ " if key in st.session_state.done else "⬜ ") + name, expanded=False):
            st.markdown(content)
            if key in st.session_state.done:
                if st.button("Mark as not completed", key="undo_"+key):
                    st.session_state.done.remove(key)
                    st.rerun()
            else:
                if st.button("Mark as completed", key="done_"+key):
                    st.session_state.done.add(key)
                    st.rerun()

st.sidebar.divider()
st.sidebar.caption("Tip: Say the answer aloud. If you cannot explain it simply, you don't own the concept yet.")
