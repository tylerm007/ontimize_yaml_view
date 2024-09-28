import { Component, ViewEncapsulation } from '@angular/core';

@Component({
  selector: 'transactions-card',
  templateUrl: './RuleConstraint-card.component.html',
  styleUrls: ['./RuleConstraint-card.component.scss'],
  encapsulation: ViewEncapsulation.None,
  host: {
    '[class.RuleConstraint-card]': 'true'
  }
})

export class RuleConstraintCardComponent {


}