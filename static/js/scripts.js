// function sortTable(n) {
//   var table, rows, switching, i, x, y, shouldSwitch, dir, switchcount = 0;
//   table = document.getElementById("myTable2");
//   switching = true;
//   // Set the sorting direction to ascending:
//   dir = "asc";
//   /* Make a loop that will continue until
//   no switching has been done: */
//   while (switching) {
//     // Start by saying: no switching is done:
//     switching = false;
//     rows = table.rows;
//     /* Loop through all table rows (except the
//     first, which contains table headers): */
//     for (i = 1; i < (rows.length - 1); i++) {
//       // Start by saying there should be no switching:
//       shouldSwitch = false;
//       /* Get the two elements you want to compare,
//       one from current row and one from the next: */
//       x = rows[i].getElementsByTagName("TD")[n];
//       y = rows[i + 1].getElementsByTagName("TD")[n];
//       /* Check if the two rows should switch place,
//       based on the direction, asc or desc: */
//       if (dir == "asc") {
//         if (x.innerHTML.toLowerCase() > y.innerHTML.toLowerCase()) {
//           // If so, mark as a switch and break the loop:
//           shouldSwitch = true;
//           break;
//         }
//       } else if (dir == "desc") {
//         if (x.innerHTML.toLowerCase() < y.innerHTML.toLowerCase()) {
//           // If so, mark as a switch and break the loop:
//           shouldSwitch = true;
//           break;
//         }
//       }
//     }
//     if (shouldSwitch) {
//       /* If a switch has been marked, make the switch
//       and mark that a switch has been done: */
//       rows[i].parentNode.insertBefore(rows[i + 1], rows[i]);
//       switching = true;
//       // Each time a switch is done, increase this count by 1:
//       switchcount ++;
//     } else {
//       /* If no switching has been done AND the direction is "asc",
//       set the direction to "desc" and run the while loop again. */
//       if (switchcount == 0 && dir == "asc") {
//         dir = "desc";
//         switching = true;
//       }
//     }
//   }
// }

blockSelect = (x,y) => location.replace(`/user/${x}/block/${y}`);
eventSelect = (x,y,z) => location.replace(`/user/${x}/block/${y}/event/${z}`);

function searchUsers() {
  var fnamesearch = users.filter(
    checkValue = (user) => user["firstname"].includes(document.getElementById("userToCheck").value));
  var lnamesearch = users.filter(
    checkValue = (user) => user["lastname"].includes(document.getElementById("userToCheck").value));
  var emailsearch = users.filter(
    checkValue = (user) => user["email"].includes(document.getElementById("userToCheck").value));
  results = removeDuplicates([...fnamesearch, ...lnamesearch, ...emailsearch]);
  if (document.getElementById("userToCheck").value.length > 0) {
    document.getElementById("user-search-results").innerHTML = "";
  	results.forEach(
      searchResults = (item) => document.getElementById(
        "user-search-results").innerHTML += `<li data-userinfo='${JSON.stringify(item)}' class="list-group-item clickable" onclick="addToForm(this)"
        >${item["lastname"]}, ${item["firstname"]}&nbsp;&lt;${item["email"]}&gt;</li>`);
  } else {
  	document.getElementById("user-search-results").innerHTML = "";
  }
}

function removeDuplicates(arr) {
  var unique = arr.reduce(function (acc, curr) {
    if (!acc.includes(curr))
      acc.push(curr);
      return acc;
  }, []);
  return unique;
}

function addToForm(user) {
  //check if user has already been added to form
  //const nodes = document.getElementById("selectedUser").childNodes;
  // var selected = [];
  // for (const child of nodes) {
  //   selected.push(child.dataset.userinfo)
  // }
  var item = JSON.parse(user.dataset.userinfo);
  var html = `<div data-userinfo='${JSON.stringify(item)}' class="alert alert-info fade show" role="alert">
    ${item["email"]}</div>`;
  document.getElementById("selectedUser").innerHTML = html;
  document.getElementById("user_email").value = item["email"];
}

// function deleteBlock(url) {
//     try {
//         const response = await fetch(url, {
//         method: "delete"
//         });
//         if (!response.ok) {
//         const message = 'Error with Status Code: ' + response.status;
//         throw new Error(message);
//         }
//         const data = await response.json();
//         console.log(data);
//     } catch (error) {
//         console.log('Error: ' + err);
//     }
// }

// function initDeleteBlockModal(element) {
//     document.getElementById("block_id").value = element.dataset.blockId;
//     document.getElementById("delete-block-title").innerHTML = element.dataset.blockTitle;
//     document.getElementById("delete-block-semester").innerHTML = element.dataset.blockSemester;
//     document.getElementById("delete-block-date-added").innerHTML = element.dataset.blockDateAdded;
//     document.getElementById("delete-block-created-by").innerHTML = element.dataset.blockCreatedBy;
//     document.getElementById("delete-block-date-modified").innerHTML = element.dataset.blockDateModified;
//     document.getElementById("delete-block-modified-by").innerHTML = element.dataset.blockModifiedBy;
//     document.getElementById("delete-block-form").action = `/user/${element.dataset.userId}/block/delete/${element.dataset.blockId}`
// }

function initAssignMemberModal(element) {
    memberId = element.dataset.memberId;
    memberRole = element.dataset.memberRole;
    document.getElementById("assign-member-form").action = `${window.location.href}/member/${memberId}/role/update`;
    document.getElementById("member_id").value = memberId;
    document.getElementById("new_role").value = memberRole;
    document.getElementById("assign-member-name").innerHTML = element.dataset.memberName;
    document.getElementById("assign-member-email").innerHTML = element.dataset.memberEmail;
    document.getElementById("assign-member-initials").innerHTML = element.dataset.memberInitials;
    document.getElementById("assign-member-type").innerHTML = element.dataset.memberType;
}

function initDeleteGuestModal(element) {
  guestId = element.dataset.guestId;
  document.getElementById("delete-guest-form").action = `${window.location.href}/guest/delete/${guestId}`;
  document.getElementById("guest_id").value = guestId;
  document.getElementById("delete-guest-name").innerHTML = element.dataset.guestName;
  document.getElementById("delete-guest-email").innerHTML = element.dataset.guestEmail;
  document.getElementById("delete-guest-initials").innerHTML = element.dataset.guestInitials;
  document.getElementById("delete-guest-notes").innerHTML = element.dataset.guestNotes;
}