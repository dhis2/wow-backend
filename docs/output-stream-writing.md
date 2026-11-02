# Java's text-to-bytes is 🤬

A drama in three acts: 
1. allocation, 
2. synchronization, 
3. and copia

### Starring: JDK `OutputStreamWriter` + `StreamEncoder`

Also featuring: your computer, crying 😭

> **[2/10] on Yelp — "would not write home with it"**

---

# It's not much but it's honest work


    Writer → OutputStreamWriter → sun.nio.cs.StreamEncoder → bytes

Each `Writer.append(int c)` call does what now? 🤨

- Wraps each `char` in a `char[]` (to call array path)
- `synchronized` — per character?
- then wraps that `char[]` in a `CharBuffer`?

**Bill: 2+ allocations and a lock acquisition per character.**

> **Rating: [0/10] "The packaging is crazy"** — your heap


---

# Send the rescue team: `BufferedWriter`™ 

```java
    new BufferedWriter(new OutputStreamWriter(out, UTF_8))
```

- Works, but hides the problem rather than solving it
- You still pay, just less

Also...
```java
    public PrintWriter(OutputStream out, boolean autoFlush, Charset charset) {
        this(new BufferedWriter(new OutputStreamWriter(out, charset)), autoFlush);
        //...
    }
```

> **Rating: [5/10] — "LGTM"** — JDK maintainers

---

# Works on my machine

```java
    new PrintWriter(out)   // Charset.defaultCharset()
```

- **Java 17:** platform default (UTF-8 on Linux, something else on some setups)
- **Java 18+:** UTF-8 by JEP 400
- Web APIs `Content-Type: application/json; charset=utf-8` might send ISO-8859-1 on JDK17

> **Rating: [2/10] "Not what I expected"** — your client

---

# Dys-copia

The issue was reported in 2009...

**16+ years of `OutputStreamWriter` + `StreamEncoder` goodness**

A lot of cope and no fix.

> **Rating: [1/10] "My DIY is 10x better"** — Jackson, Netty, Okio, and every performance engineer since 2010 🧤

---

# Down the `Appender`-sink

What if... we just send what we got?

```java
    void appendAscii(char c);
    void appendAscii(CharSequence, int, int);

    void appendEncoded(char c);
    void appendEncoded(CharSequence, int, int);

    void appendJsonEscaped(CharSequence);

    void appendInt(int value);
    void appendLong(long value);
    void appendDouble(double value);
```

> **Rating: [7/10] "A bit primitive, but works well"** — bro-grammers

---

# Out now: `OutputStream`-ZERO

No garbage in it! `Appender.ofUTF8(OutputStream)`

- UTF-8 encoded in-line into a reusable 8 KiB `byte[]` buffer
- No `CharsetEncoder`, no `CharBuffer`, no intermediate `char[]`
- Surrogate pairs always handled correctly

> **Rating: [11/10] "👍 not the usual garbage"** — DHIS2 admins


---

# Look, ma! No `String`s needed

`Appender.of` => `TextBuilder` => `textValue()` => `Text`

- Same API, `char[]` internally, yields immutable `Text` view
- Inherits `AutoCloseable` but does not need `try`-with-resources
- `CharSequence`-ify all the things with `Text`
- `Text.copyTo`-fast-path

> **Rating: [9/10] "I want a `slice` of that"** — String

---

# Widening your horizon

Why having both is essential
```java
    float f = 0.1
    out.appendFloat(f);  // "0.1"
    out.appendDouble(f); // "0.10000000149011612"
```
JDK formatting only accessible via `toString()` with 
several extra allocations 😖

> `**Rating: [NaN/10.0001] "Extra bits for free, W"** — Your CPU

---

# That escalated quickly...

- **Data export JSON** (`DataExportOutput`) — 1M values/s range
- **Data export CSV** (`CsvBuilder` + `Utf8OutputStreamAppender`)
- **Gist API JSON + CSV** (`GistOutput`, `JsonStreamOutput`)
- **Period types output** (`PeriodOutput`)
- **OpenAPI HTML, JSON, YAML** (`OpenApiController`, `OpenApiGenerator`, `OpenApiRenderer`)
- **JSON builder in json-tree** (`JsonBuilder.streamArray` / `streamObject`)

> **Rating: [10/10] "You feel so clean afterwards"** — me

---

# The End


> **Fun fact: "100% of memory wasted is later recycled"** — OOM
