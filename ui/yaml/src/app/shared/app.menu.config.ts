import { MenuRootItem } from 'ontimize-web-ngx';

import { EntityCardComponent } from './Entity-card/Entity-card.component';

import { EntityAttrCardComponent } from './EntityAttr-card/EntityAttr-card.component';

import { GlobalSettingCardComponent } from './GlobalSetting-card/GlobalSetting-card.component';

import { TabGroupCardComponent } from './TabGroup-card/TabGroup-card.component';

import { TemplateCardComponent } from './Template-card/Template-card.component';

import { YamlFilesCardComponent } from './YamlFiles-card/YamlFiles-card.component';


export const MENU_CONFIG: MenuRootItem[] = [
    { id: 'home', name: 'HOME', icon: 'home', route: '/main/home' },
    { id: 'settings', name: 'Settings', icon: 'settings', route: '/main/settings'},
    { id: 'data', name: 'Yaml Data', icon: 'remove_red_eye', opened: true,
    items: [
        { id: 'Entity', name: 'ENTITY', icon: 'description', route: '/main/Entity' }
        ,{ id: 'EntityAttr', name: 'ENTITYATTR', icon: 'description', route: '/main/EntityAttr' }
        ,{ id: 'TabGroup', name: 'TABGROUP', icon: 'description', route: '/main/TabGroup' }
    
        ] 
    }
    ,{ id: 'other', name: 'Global', icon: 'remove_red_eye', opened: false,
    items: [        
        { id: 'GlobalSetting', name: 'GLOBALSETTING', icon: 'description', route: '/main/GlobalSetting' }
        ,{ id: 'Template', name: 'TEMPLATE', icon: 'description', route: '/main/Template' }
        ] 
    }
    ,{ id: 'YamlFiles', name: 'YAMLFILES', icon: 'upload_file', route: '/main/YamlFiles' }
    ,{ id: 'about', name: 'About', icon: 'info', route: '/main/about'}
    ,{ id: 'logout', name: 'LOGOUT', route: '/login', icon: 'power_settings_new', confirm: 'yes' }
];

export const MENU_COMPONENTS = [

    EntityCardComponent

    ,EntityAttrCardComponent

    ,GlobalSettingCardComponent

    ,TabGroupCardComponent

    ,TemplateCardComponent

    ,YamlFilesCardComponent

];