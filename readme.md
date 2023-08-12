# hi, a human interpreter

> A truly natural scripting language
>
hi runs your natural language

## Example
```
hi could you list current dir
```
since ? is special character in shell, if you want to use ?, just add quotation mark around it,like this
```
hi "could you list current dir?"
```
hi can also be used as shellbang interpreter
```shell
progressbar.hi
#!/usr/bin/env hi
could you display a progress bar from 1 to 100?
```

It can be executed like any other script.

```shell
$ ./progressbar.hi

```



```shell
#!/usr/bin/env bash

echo "Progress:"

for ((i=1; i<=100; i++))
do
    echo -ne "$i%\r"
    sleep 0.1
done

echo "Complete!"%  
```

The code is streamed out of the LLM during inferpretation and executed line by line so execution is not blocked waiting for inference to finish. The generated code is cached on first run and will be executed instantly on subsequent runs, bypassing the need for reinferpretation.

You can see it in action here:

![](demo.svg)

## Usage

### Install humanscript

You can run humanscript in a sandboxed environment via Docker:

```shell
docker run -it lukechilds/humanscript
```

Alternatively you can install it natively on your system with Homebrew:

```shell
brew install lukechilds/tap/humanscript
```

Or manually install by downloading this repository and copy/symlink `humanscript` into your PATH.

> Be careful if you're running humanscript unsandboxed. The inferpreter can sometimes do weird and dangerous things. Speaking from experience, unless you want to be doing a system restore at 2am on a saturday evening, you should atleast run humanscripts initially with `HUMANSCRIPT_EXECUTE="false"` so you can check the resulting code before executing.

### Write and execute a humanscript

humanscript is configured out of the box to use OpenAI's GPT-4, you just need to add your API key.

We need to add it to `~/.humanscript/config`

```shell
mkdir -p ~/.humanscript/
echo 'HUMANSCRIPT_API_KEY="<your-openai-api-key>"' >> ~/.humanscript/config
```

Now you can create a humanscript and make it executable.

```shell
echo '#!/usr/bin/env humanscript
print an ascii art human' > asciiman
chmod +x asciiman
```

And then execute it.

```shell
./asciiman
  O
 /|\
 / \
```

## Configuration

All environment variables can be added to `~/.humanscript/config` to be applied globally to all humanscripts:

```shell
$ cat ~/.humanscript/config
HUMANSCRIPT_API_KEY="sk-XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
HUMANSCRIPT_MODEL="gpt-4"
```

or on a per script basis:

```shell
$ HUMANSCRIPT_REGENERATE="true" ./asciiman
```

### `HUMANSCRIPT_API`

Default: `https://api.openai.com/v1`

A server following OpenAI's Chat Completion API.

Many local proxies exist that implement this API in front of locally running LLMs like Llama 2. [LM Studio](https://lmstudio.ai/) is a good option.

```shell
HUMANSCRIPT_API="http://localhost:1234/v1"
```

### `HUMANSCRIPT_API_KEY`

Default: `unset`

The API key to be sent to the LLM backend. Only needed when using OpenAI.

```shell
HUMANSCRIPT_API_KEY="sk-XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
```

### `HUMANSCRIPT_MODEL`

Default: `gpt-4`

The model to use for inference.

```shell
HUMANSCRIPT_MODEL="gpt-3.5"
```

### `HUMANSCRIPT_EXECUTE`

Default: `true`

Whether or not the humanscript inferpreter should automatically execute the generated code on the fly.

If false the generated code will not be executed and instead be streamed to stdout.

```shell
HUMANSCRIPT_EXECUTE="false"
```

### `HUMANSCRIPT_REGENERATE`

Default: `false`

Whether or not the humanscript inferpreter should regenerate a cached humanscript.

If true the humanscript will be reinferpreted and the cache entry will be replaced with the newly generated code. Due to the nondeterministic nature of LLMs each time you reinferpret a humanscript you will get a similar but slightly different output.

```shell
HUMANSCRIPT_REGENERATE="true"
```

## License

MIT © Luke Childs
