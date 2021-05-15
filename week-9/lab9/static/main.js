const birthdayService = {
    delete: (id) => {
        return new Promise((resolve, reject) => {
            $.ajax({
                method: "DELETE",
                url: "/",
                data: { id },
            }).done(() => {
                resolve()
            }).fail((error) => {
                reject(error)
            })
        })
    }
}

function removeBirthday(id){
    birthdayService.delete(id)
        .then(() => {
            removeBirthdayRow(id)
        })
        .catch(error => {
            console.error(error)
        })
}

function removeBirthdayRow(id){
    const birthdayRow = document.getElementById(`birthday-${id}`)
    document.getElementById("birtday-rows").removeChild(birthdayRow)
}