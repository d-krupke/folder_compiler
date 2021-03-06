# A simple folder compiler

A simple python util to 'compile' a folder, e.g. for static webpages.

The primary thing this tool does is to walk through a directory, applying provided
`processors` until the first one accepts it, some basic utils to read/write/check files, 
and keeping track of which file has been created by which.

For example go through the input directory, compile all markdown files from the input
directory to html in the output directory, and copy all images.

Or compress all flac files in the input directory to ogg in the ouput directory.
Skipping if the output is newer than the input and deleting orphaned files in the output.

## Install

[pip](https://pypi.org/project/folder-compiler/) or simply clone it and copy the folder.
That way you can easily adapt it to your own needs (you are free to steal this code as 
long as you don't make me responsible for anything).

## Example: Compiling a static webpage

This has been my primary motivation to develop this util.
The existing static webpage compiler have been simply too powerful and complicated for
my simple use case in which I just wanted to compile the markdown files to html and
add a navigation bar.
This can be achieved by simple using a markdown compiler and the Jinja template engine.
Compiling bibtex files to a publications page and stuff like that can also be easily integrated.

The corresponding modules are part of a separate [repository](https://github.com/d-krupke/folder_compiler_static_website).

## Example: Compressing Music

This util can also be used to compress your flac music library to ogg for your phone.
It skips already compressed files and deletes files that are no longer in the library.

```python
import os
import subprocess
import shlex
import folder_compiler
from folder_compiler.processors import Processor, ProcessorUtils, FileCopyProcessor


class FlacToOggProcessor(Processor):
    """
    This processor compresses flac files to ogg.
    """

    def process_file(self, source: str, utils: ProcessorUtils):
        target = os.path.splitext(source)[0] + ".ogg"  # change file extension of target
        utils.add_file(target)  # do not delete this file!
        if utils.is_target_outdated(source=source, target=target):  # only if source is newer
            source_file = utils.get_full_source_path(source)  # get full path
            target_file = utils.get_full_target_path(target)  # get full path
            # oggenc command
            cmd = " ".join(
                ["oggenc", "-q", "8", shlex.quote(source_file), "-o",
                 shlex.quote(target_file)])
            # execute
            print(cmd)
            subprocess.run(cmd, check=True, shell=True)
        return True  # The file has been processed


processors = [
    FlacToOggProcessor().add_include(".*\.flac"),  # compress flacs
    FileCopyProcessor().add_include(".*\.jpg").add_include(".*\.png")  # copy cover images
]

# Paths: From where should the music compiled to where
uncompressed_music_source = "/home/krupke/Music"
compressed_music_target = "/path/to/my/phones/sd"
compiler = folder_compiler.FolderCompiler(input=uncompressed_music_source,
                               output=compressed_music_target)

compiler.compile(processors)  # performs the compression
compiler.remove_orphaned_files()  # remove files that are not owned by any processor
```