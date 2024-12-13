import { MenuRootItem } from 'ontimize-web-ngx';

import { EntityCardComponent } from './Entity-card/Entity-card.component';

import { EntityAttrCardComponent } from './EntityAttr-card/EntityAttr-card.component';

import { GlobalSettingCardComponent } from './GlobalSetting-card/GlobalSetting-card.component';

import { RuleConstraintCardComponent } from './RuleConstraint-card/RuleConstraint-card.component';

import { RuleDerivationCardComponent } from './RuleDerivation-card/RuleDerivation-card.component';

import { RuleEventCardComponent } from './RuleEvent-card/RuleEvent-card.component';

import { TabGroupCardComponent } from './TabGroup-card/TabGroup-card.component';

import { TemplateCardComponent } from './Template-card/Template-card.component';

import { YamlFilesCardComponent } from './YamlFiles-card/YamlFiles-card.component';


export const MENU_CONFIG: MenuRootItem[] = [
    { id: 'home', name: 'HOME', icon: 'home', route: '/main/home' },
    { id: 'New YamlFiles', name: '1. Import Project', icon: 'upload', route: '/main//YamlFiles/new' },
    { id: 'YamlFiles', name: '2. Select Working App', icon: 'upload_file', route: '/main/YamlFiles' },
    { id: 'data', name: '3. Edit Data', icon: 'edit_square', opened: true,
    items: [
        { id: 'Entity', name: 'Entities', icon: 'view_list', route: '/main/Entity' , component: EntityCardComponent}
        ,{ id: 'EntityAttr', name: 'Attributes', icon: 'view_list', route: '/main/EntityAttr' , component: EntityAttrCardComponent}
        ,{ id: 'TabGroup', name: 'Relationships', icon: 'view_list', route: '/main/TabGroup', component: TabGroupCardComponent}
    
        ] 
    }
    ,{id: 'rules', name: 'Rules', icon: 'edit_square', opened: false,
    items: [
        { id: 'RuleConstraint', name: 'Constraints', icon: 'view_list', route: '/main/RuleConstraint' }
        ,{ id: 'RuleDerivation', name: 'Derivations', icon: 'view_list', route: '/main/RuleDerivation' }
        ,{ id: 'RuleEvent', name: 'Events', icon: 'view_list', route: '/main/RuleEvent' }
        ] 
    }
    ,{id:'security', name: 'Security', icon: 'security', opened: false,
    items: [
            { id: 'Role', name: 'User Roles', icon: 'view_list', route: '/main/RbacRole' }
            ,{ id: 'GrantRole', name: 'Grants', icon: 'view_list', route: '/main/GrantRole' }
        ]
    }
    ,{ id: 'Application', name: 'Application', icon: 'view_list', route: '/main/Application', opened: false,
    items: [
        { id: 'Application', name: 'Applications', icon: 'view_list', route: '/main/Application'}
        ,{ id: 'ApplicationEntity', name: 'Application Entities', icon: 'view_list', route: '/main/ApplicationEntity'}
    ]
    }
    ,{ id: 'YamlFiles', name: '4. Download Model Files', icon: 'download_file', route: '/main/DownloadYamlFiles' }
    ,{ id: 'other', name: 'Global Settings', icon: 'remove_red_eye', opened: false,
        items: [        
            { id: 'GlobalSetting', name: 'Global Settings', icon: 'view_list', route: '/main/GlobalSetting' }
            ,{ id: 'Template', name: 'Input Components', icon: 'view_list', route: '/main/Template' }
            ]
    }, 
    { id: 'settings', name: 'Settings', icon: 'settings', route: '/main/settings'}
    ,{ id: 'about', name: 'About', icon: 'info', route: '/main/about'}
    ,{ id: 'logout', name: 'LOGOUT', route: '/login', icon: 'power_settings_new', confirm: 'yes' }
];

export const MENU_COMPONENTS = [

    EntityCardComponent

    ,EntityAttrCardComponent

    ,GlobalSettingCardComponent

    ,RuleConstraintCardComponent

    ,RuleDerivationCardComponent

    ,RuleEventCardComponent

    ,TabGroupCardComponent

    ,TemplateCardComponent

    ,YamlFilesCardComponent

];