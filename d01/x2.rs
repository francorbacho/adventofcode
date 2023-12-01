use std::collections::HashMap;
use std::fs;

fn extract_first_last(line: &str) -> (usize, usize) {
    let numerics = (0..=9).map(|x| x.to_string()).enumerate();
    let numerals = ["zero", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine"];
    let numerals = numerals.iter().map(|x| x.to_string()).enumerate();
    let numbers = numerals.chain(numerics).map(|(i, v)| (v, i)).collect::<HashMap<String, usize>>();

    let keys = numbers.keys().filter(|k| line.contains(&**k));

    let first = keys.clone().min_by_key(|k| line.find(&**k).unwrap());
    let last = keys.max_by_key(|k| line.rfind(&**k).unwrap());

    (*numbers.get(first.unwrap()).unwrap(), *numbers.get(last.unwrap()).unwrap())
}

fn main() {
    let contents = fs::read_to_string("input.txt").expect("read");
    let result: usize = contents
        .split('\n')
        .filter(|line| !line.is_empty())
        .inspect(|x| println!("about to filter: {x}"))
        .map(|line| extract_first_last(line))
        .inspect(|x| println!("about to filter: {x:?}"))
        .map(|(f, l)| f * 10 + l)
        .sum();
    println!("result: {result}");
}
