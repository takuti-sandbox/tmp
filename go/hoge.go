type ButtleShip interface {
  HP() float32
  SetHP(v float32
  Fire() float32
  Shield() float32
}

type KanMusume struct {
  // TOOD: implement ButtleShip interface
}

func Bombard(attacker, defender ButtleShip) float32 {
  // Calculate damage
  damage := attacker.Fire() * rand.Float32()
  damage -= defender.Shield() * rand.Float32()
  if damage < 0.0 {
    damage = 0.0
  }
  // Update defender's HP
  remain := defender.HP() - damage
  if remain < 0.0 {
    remain = 0.0
  }
  defender.SetHP(remain)
  return damage
}

func (*KanMusume) HP() float32 {
  // TOOD: implement me.
  return 0.0
}
func (*KanMusume) SetHP(float32) {
  // TOOD: implement me.
}
func (*KanMusume) Fire() float32 {
  // TOOD: implement me.
  return 0.0
}
func (*KanMusume) Shield() float32 {
  // TOOD: implement me.
  return 0.0
}
