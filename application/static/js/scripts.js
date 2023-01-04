
/**
 * SmartInterval
 * https://github.com/4skinSkywalker/SmartInterval
 */

function SmartInterval(asyncFn, delayMs) {
  this.asyncFn = asyncFn;
  this.delayMs = delayMs;

  this.running = false;
}

SmartInterval.prototype.cycle = async function (forced) {
  await this.asyncFn();
  await this.delay(this.delayMs);
  if (!forced && this.running) this.cycle();
};

SmartInterval.prototype.start = function () {
  if (this.running) return;
  this.running = true;
  this.cycle();
};

SmartInterval.prototype.stop = function () {
  if (this.running) this.running = false;
};

SmartInterval.prototype.forceExecution = function () {
  if (this.running) this.cycle(true);
};

// This function is just an arbitrary delay to be used with async/await pattern
SmartInterval.prototype.delay = function (ms) {
  return new Promise(res =>
    setTimeout(() => res(1), ms)
  );
};
// ==================== End SmartInterval ========================


// ==================== On DOMContentLoaded ========================
window.addEventListener('DOMContentLoaded', event => {
  // Toggle the side navigation
  const sidebarToggle = document.body.querySelector('#sidebarToggle');
  if (sidebarToggle) {
    // Uncomment Below to persist sidebar toggle between refreshes
    // if (localStorage.getItem('sb|sidebar-toggle') === 'true') {
    //     document.body.classList.toggle('sb-sidenav-toggled');
    // }
    sidebarToggle.addEventListener('click', event => {
      event.preventDefault();
      document.body.classList.toggle('sb-sidenav-toggled');
      localStorage.setItem('sb|sidebar-toggle', document.body.classList.contains('sb-sidenav-toggled'));
    });
  }

  // =================== unread message menu ============================
  let unreadMsgMenuColor = document.getElementById('unread-message-menu-color');
  let unreadMsgMenuList = document.getElementById('unread-message-menu-list');
  let unreadMsgMenuCount = document.getElementById('unread-message-menu-count');

  const getUnreadMessageList = async () => {
    let api_url = `/conversation/get-unread`;
    try {
      let response = await fetch(api_url);
      let unreadMsgList = await response.json();

      unreadMsgMenuCount.innerHTML = unreadMsgList.length;
      let menuItems = '';
      if (unreadMsgList.length) {
        unreadMsgMenuColor.classList.remove("bg-danger");
        unreadMsgMenuColor.classList.add("bg-danger");
        for (u of unreadMsgList) {
          let tmpl = `<li class='border-top'><a class="dropdown-item" href="/conversation/${u.patient_username}">${u.patient_fullname}<br><small>${u.created_at}</small></a></li>`
          menuItems += tmpl;
        }
        unreadMsgMenuList.innerHTML = menuItems;
      } else {
        unreadMsgMenuColor.classList.remove("bg-danger");
        unreadMsgMenuList.innerHTML = `<li><a class="dropdown-item" href="javascript:void(0)">No unread message.</a></li>`;
      }
    } catch (e) {
      console.log('Could not retrieve latest conversation.');
      console.log('Retrying...');
      return [];
    }
  }

  // =================== mark message red or unread ============================
  let READ_STATUS = ['&#9679; Mark as read', '&#9711; Mark as unread']
  let readStatusLinks = document.querySelectorAll('.read-status');
  for (readStatusLink of readStatusLinks) {
    readStatusLink.addEventListener('click', async (event) => {
      let convId = event.target.dataset.id;
      let readStatus = event.target.dataset.status;
      let api_url = `/conversation/set-read-status/${convId}/${readStatus}`;
      let response = await fetch(api_url)
      let data = await response.text();

      event.target.dataset.status = data;
      event.target.text = new DOMParser().parseFromString(READ_STATUS[data], "text/html").documentElement.textContent;
      await getUnreadMessageList();
    });
  }

  // =================== show unread message count in regullar interval =============
  let unreadFetchInterval = (5 * 60 * 1000) // 5 min

  let dataFetcher = new SmartInterval(
    async () => {
      await getUnreadMessageList();
      console.log(new Date())
    },
    unreadFetchInterval
  );

  dataFetcher.start();

});
// ==================== On DOMContentLoaded Ends ========================