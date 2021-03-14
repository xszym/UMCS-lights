const Segment = ({ color, id }) => {

  const getColorRGBA = (color) => {
    let rgb_sum = color[0] + color[1] + color[2];
    let transp = rgb_sum / (255 * 3);

    // if(!color[0] && !color[1] && !color[2]) return `${color}, 0.3`;
    return `${color}, ${transp}`;
  }

  const ifDisabled = (id) => {
    return (id >= 0 && id <= 10);
  }

  let opacity = 1;
  if (ifDisabled(id)) opacity = 0.7;

  return (
    <div
      style={{
        // borderStyle: "solid",
        // borderRadius:'3px',
        // borderWidth: "1px",
        opacity: {opacity},
        width: "30px",
        height: "70px",
        minWidth: "15px",
        backgroundColor: `rgba(${color}, ${opacity})`,
        // background: `linear-gradient(to bottom, rgba(${this.getColorRGBA(color)}), rgba(${color},0))`,
        // background: `linear-gradient(to bottom, rgba(${color},1), rgba(${color},0))`,
        margin: "3px"
      }}
    >
    </div>
  )
};

export default Segment;
