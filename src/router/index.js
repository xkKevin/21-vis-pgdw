import Vue from 'vue'
import VueRouter from 'vue-router'
import Home from '../views/Home.vue'

Vue.use(VueRouter)

const routes = [{
        path: '/',
        name: 'Home',
        component: () =>
            import ('@/views/showGlyphs'),
        // redirect: ''
    },
    {
        path: '/about',
        name: 'About',
        // route level code-splitting
        // this generates a separate chunk (about.[hash].js) for this route
        // which is lazy-loaded when the route is visited.
        component: () =>
            import ( /* webpackChunkName: "about" */ '../views/About.vue')
    },
    {
        path: '/showGlyphs',
        name: 'ShowGlyphs',
        component: () =>
            import ('@/views/showGlyphs')
    },
    {
        path: '/upload',
        name: 'UploadTables',
        component: () =>
            import ('@/views/InputTables')
    }
]

const router = new VueRouter({
    mode: 'hash', //'history',
    base: process.env.BASE_URL,
    routes
})

export default router