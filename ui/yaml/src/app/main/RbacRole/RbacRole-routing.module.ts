import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { RbacRoleHomeComponent } from './home/RbacRole-home.component';
import { RbacRoleNewComponent } from './new/RbacRole-new.component';
import { RbacRoleDetailComponent } from './detail/RbacRole-detail.component';

const routes: Routes = [
  {path: '', component: RbacRoleHomeComponent},
  { path: 'new', component: RbacRoleNewComponent },
  { path: ':name', component: RbacRoleDetailComponent,
    data: {
      oPermission: {
        permissionId: 'RbacRole-detail-permissions'
      }
    }
  },{
    path: ':role_name/GrantRole', loadChildren: () => import('../GrantRole/GrantRole.module').then(m => m.GrantRoleModule),
    data: {
        oPermission: {
            permissionId: 'GrantRole-detail-permissions'
        }
    }
}
];

export const RBACROLE_MODULE_DECLARATIONS = [
    RbacRoleHomeComponent,
    RbacRoleNewComponent,
    RbacRoleDetailComponent 
];


@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class RbacRoleRoutingModule { }