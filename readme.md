# hi, a human interpreter

> A truly natural scripting language
>
hi runs your natural language

### Install humanscript
hi script is provided in python-hi pip package
```shell
pip install -U python-hi
```

you can also clone this repository and run "poetry install"

> Be careful The converted bash can contain weird things.
> you can run hi script initially with HI_EXECUTE=false
> to check the resulting code before executing.

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

The code is sent to LLM and then convert to bash and then execute, while also cache for next time fast reexecute(then it doesn't 
need to query the LLM again)



## Usage



### Config hi

We need to add it to `~/.hi`

```
HI_API_KEY: sk-xxx
HI_MODEL: gpt-4
#HI_API: if you have a different base to forward other than https://api.openai.com/v1, it's set using openai.openai_api_base=this value
```

Now you can run hi script either from command line or as an shellbang interpreter(check out samples/*.hi)

### Cache invalidation
after you first run the script, the converted bash code will be cached in ~/.hicache/ , you can run
```shell
hi cache clear
```
to completely clear the cache.

### Configuration that can change runtime behavior
you can set the following variables in ~/.hi(in yaml format) or use in command line like 
```shell
$ HI_API_KEY="sk-xxx" hi ...
```
### `HI_EXECUTE`
you can use HI_EXECUTE to control the execution of the hi script
```shell
$ HI_EXECUTE="false" hi ...
```

### `HI_API`

Default: `https://api.openai.com/v1`

A server following OpenAI's Chat Completion API.

Many local proxies exist that implement this API in front of locally running LLMs like Llama 2. [LM Studio](https://lmstudio.ai/) is a good option.

```shell
HI_API="http://localhost:1234/v1"
```

### `HI_API_KEY`

Default: `unset`

The API key to be sent to the LLM backend. Only needed when using OpenAI.

```shell
HI_API_KEY="sk-XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
```

### `HI_MODEL`

Default: `gpt-4`

The model to use for inference.

```shell
HI_MODEL="gpt-3.5"
```

### `HI_EXECUTE`

Default: `true`

Whether or not the hi interpreter should automatically execute the generated code on the fly.

If false the generated code will not be executed and instead be streamed to stdout.

```shell
HI_EXECUTE="false"
```

### `HI_REGENERATE`

Default: `false`

Whether or not the hi interpreter should regenerate a cached hiscript.

If true the hiscript will be reinterpreted and the cache entry will be replaced with the newly generated code. Due to the nondeterministic nature of 
LLMs each time you reinferpret a hiscript you will get a similar but slightly different output.

```shell
HI_REGENERATE="true"
```

## Inspiration
This project is highly inspired by humanscript project(https://github.com/lukechilds/humanscript), but I think hi is a better name,
also hi can be interpreted as short for human input, human inteprete,human interface, human inferenceinterpreter etc,
and just for fun.
Also using python is easier for plugin architecture, the way I think is in different project/workspace, maybe there will be
different 'hi' implementations, so .hi in that directory with plugin_type="metagpt" will run some metagpt command at that directory.

## License

MIT © femto Zheng
