import {tournaments} from '/views/tournaments.js';
import {tournament} from '/views/tournament.js';
import {tournamentEdit} from '/views/tournamentEdit.js';
import {gameDate} from '/views/gameDate.js';
import {pitch} from '/views/pitch.js';
import {gameEditor} from '/views/gameEditor.js';
import {statistics} from '/views/statistics.js';
import {information} from '/views/information.js';
import {login} from '/views/login.js';
import {loginUser} from '/views/loginUser.js';
import {about} from '/views/about.js';
import {GoogleUser} from '/html/googleSignIn.js';

const routes = [
  { path: '/', component: tournaments },
  { path: '/tournaments', component: tournaments },
  { path: '/:id', component: tournament },
  { path: '/tournament/:id', component: tournament },
  { path: '/tournament/:id/edit', component: tournamentEdit },
  { path: '/statistics/:id', component: statistics },
  { path: '/information/:id', component: information },
  { path: '/login', component: login },
  { path: '/about', component: about }
]

Vue.component('gameDate', gameDate)
Vue.component('pitch', pitch)
Vue.component('gameEditor', gameEditor)
Vue.component('loginUser', loginUser)

const router = new VueRouter({ routes })

Vue.prototype.$googleUser = new GoogleUser();
Vue.prototype.$googleUser.appStart();

const app = new Vue({ router });

app.$mount('#app');