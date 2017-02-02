#![allow(unused_must_use)]
use std::os;
use std::io::{File, IoResult, IoError, EndOfFile};
use std::io::stdio::{stdout_raw, stderr};

fn main() {
    let paths = os::args().slice_from_or_fail(&1).to_vec();
    let mut stderr = stderr();

    if paths.len() < 1 {
        stderr.write_str("file name not given\n");
    }
    for path in paths.iter() {
        let res = do_cat(path);
        if res.is_err() {
            panic!("{}: {}", path, res.unwrap_err());
        }
    }
}

const BUFFER_SIZE: uint = 2048;

fn do_cat(path: &String) -> IoResult<()> {
    let mut writer = stdout_raw();
    let mut in_buf = [0, .. BUFFER_SIZE];
    let mut reader = File::open(&std::path::Path::new(path));

    loop {
        let n = match reader.read(&mut in_buf) {
            Ok(n) if n == 0 => return Ok(()),
            Ok(n) => n,
            Err(IoError{ kind: EndOfFile, ..}) => return Ok(()),
            Err(e) => return Err(e)
        };
        try!(writer.write(in_buf.slice_to(n)));
    }
}
