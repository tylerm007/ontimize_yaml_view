import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { GrantRoleHomeComponent } from './home/GrantRole-home.component';
import { GrantRoleNewComponent } from './new/GrantRole-new.component';
import { GrantRoleDetailComponent } from './detail/GrantRole-detail.component';

const routes: Routes = [
  {path: '', component: GrantRoleHomeComponent},
  { path: 'new', component: GrantRoleNewComponent },
  { path: ':entity_name/:role_name', component: GrantRoleDetailComponent,
    data: {
      oPermission: {
        permissionId: 'GrantRole-detail-permissions'
      }
    }
  }
];

export const GRANTROLE_MODULE_DECLARATIONS = [
    GrantRoleHomeComponent,
    GrantRoleNewComponent,
    GrantRoleDetailComponent 
];


@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class GrantRoleRoutingModule { }