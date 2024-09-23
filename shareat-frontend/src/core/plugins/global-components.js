import Vue from 'vue';

import SidebarModal from '@/core/ui/components/shared/sidebar-modal/SidebarModal.vue';
import SidebarModalWrapper from '@/core/ui/components/shared/sidebar-modal/SidebarContentWrapper.vue';

import CenterModal from '@/core/ui/components/shared/center-modal/CenterModal.vue';
import CenterModalContentWrapper from '@/core/ui/components/shared/center-modal/CenterModalContentWrapper.vue';

Vue.component('SidebarModal', SidebarModal);
Vue.component('SidebarModalWrapper', SidebarModalWrapper);
Vue.component('CenterModal', CenterModal);
Vue.component('CenterModalContentWrapper', CenterModalContentWrapper);
