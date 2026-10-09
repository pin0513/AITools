// 屬性條件運算子(對照組:現行只有「等於 / 不等於」,沒有「包含 / 不包含」)
export function getOperatorList(type: string) {
  const ops = [
    { value: 'EQUAL', label: '等於' },
    { value: 'NOT_EQUAL', label: '不等於' },
  ];
  return ops;
}

export class ConditionForm {
  operator = 'EQUAL';
}
