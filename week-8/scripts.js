const hobbies = {
    games: () => window.prompt('type a game:'),
    guitar: () => window.prompt('type a music:'),
    books: () => window.prompt('type a book:'),
    moviesandseries: () => window.prompt('type something'),
}

function sanitize(text) {
    if(!text) {
        console.error(`No text to sanitize!`)
        return;
    }

    return text
        .toLowerCase()
        .replace(/ /g, '')
        .trim()
}

function hobbieSelected(element) {
    const value = sanitize(element.innerHTML)

    // guard against not implemented values
    if(!hobbies[value]) {
        console.error(`Not found: action for hobbie ${value}`)
        return;
    }

    const action = hobbies[value]
    const answer = action()

    alert(`${answer} is a cool answer!`)
}

function main() {
    document.querySelectorAll(['[card]']).forEach(el => {
        el.addEventListener('click', () => hobbieSelected(el))
    })
}

document.addEventListener('DOMContentLoaded', main)