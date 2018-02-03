use std::io::prelude::*;

use std::env;
use std::fs::File;
use std::collections::HashMap;
use std::process::Command;


struct Brucefile {
    content: String,
    commands: HashMap<String, String>,
}

impl Brucefile {

    fn from_file(filename: &str) -> Brucefile {
        let content = load(filename);
        let mut cmds: HashMap<String, String> = HashMap::new();

        content.split('\n').for_each(|line| {
            let words: Vec<&str> = line.split(':').collect();

            if words.len() == 2 {
                cmds.insert(String::from(words[0]), String::from(words[1]));
            }
        });

        Brucefile { content: content, commands: cmds }
    }

    fn run(&self, cmd_name: &str) -> String {
        let cmd = &self.commands[cmd_name].trim();

        match Command::new(cmd).output() {
            Ok(output) => String::from_utf8_lossy(&output.stdout).into_owned(),
            Err(e) => {
                println!("{}", e);
                String::from("Err")
            }
        }
    }

}


fn load(filename: &str) -> String {
    let f = File::open(filename);
    let mut buffer = String::new();

    match f.ok() {
        Some(mut v) => {v.read_to_string(&mut buffer);},
        None => {},
    }

    return buffer;
}

fn get_cmd() -> String {
    match env::args().nth(1) {
        Some(cmd) => cmd,
        None => String::from("_no_command")
    }
}

fn main() {
    let brucefile = Brucefile::from_file("Brucefile");

    let output = brucefile.run(get_cmd().as_str());

    println!("{}", output);
}
