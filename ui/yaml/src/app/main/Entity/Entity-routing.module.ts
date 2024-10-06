import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { EntityHomeComponent } from './home/Entity-home.component';
import { EntityNewComponent } from './new/Entity-new.component';
import { EntityDetailComponent } from './detail/Entity-detail.component';

const routes: Routes = [
  {path: '', component: EntityHomeComponent},
  { path: 'new', component: EntityNewComponent },
  { path: ':name', component: EntityDetailComponent,
    data: {
      oPermission: {
        permissionId: 'Entity-detail-permissions'
      }
    }
  },{
    path: ':entity_name/EntityAttr', loadChildren: () => import('../EntityAttr/EntityAttr.module').then(m => m.EntityAttrModule),
    data: {
        oPermission: {
            permissionId: 'EntityAttr-detail-permissions'
        }
    }
},{
    path: ':entity_name/RuleConstraint', loadChildren: () => import('../RuleConstraint/RuleConstraint.module').then(m => m.RuleConstraintModule),
    data: {
        oPermission: {
            permissionId: 'RuleConstraint-detail-permissions'
        }
    }
},{
    path: ':as_child_entity/RuleDerivation', loadChildren: () => import('../RuleDerivation/RuleDerivation.module').then(m => m.RuleDerivationModule),
    data: {
        oPermission: {
            permissionId: 'RuleDerivation-detail-permissions'
        }
    }
},{
    path: ':entity_name/RuleDerivation', loadChildren: () => import('../RuleDerivation/RuleDerivation.module').then(m => m.RuleDerivationModule),
    data: {
        oPermission: {
            permissionId: 'RuleDerivation-detail-permissions'
        }
    }
},{
    path: ':entity_name/RuleEvent', loadChildren: () => import('../RuleEvent/RuleEvent.module').then(m => m.RuleEventModule),
    data: {
        oPermission: {
            permissionId: 'RuleEvent-detail-permissions'
        }
    }
},{
    path: ':entity_name/TabGroup', loadChildren: () => import('../TabGroup/TabGroup.module').then(m => m.TabGroupModule),
    data: {
        oPermission: {
            permissionId: 'TabGroup-detail-permissions'
        }
    }
},{
    path: ':tab_entity/TabGroup', loadChildren: () => import('../TabGroup/TabGroup.module').then(m => m.TabGroupModule),
    data: {
        oPermission: {
            permissionId: 'TabGroup-detail-permissions'
        }
    }
}
];

export const ENTITY_MODULE_DECLARATIONS = [
    EntityHomeComponent,
    EntityNewComponent,
    EntityDetailComponent 
];


@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class EntityRoutingModule { }