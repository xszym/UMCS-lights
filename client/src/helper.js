export const initValues = () => {
  let values = [];
  for (let i = 0; i < 5; i++) {
    let tmp = []
    for (let j = 0; j < 28; j++) {
      tmp.push([0, 0, 0]);
    }
    values.push(tmp);
  }
  return values;
}
