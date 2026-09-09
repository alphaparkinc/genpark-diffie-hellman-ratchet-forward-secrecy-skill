"""Example usage for Double Ratchet Skill."""
from client import DoubleRatchetSession

def main():
    print("Executing Double Ratchet Forward Secrecy...")
    session = DoubleRatchetSession("AGENT_SWARM_GENESIS_SECRET")
    c1 = session.encrypt_and_ratchet("Directive: Move to Sector 7")
    c2 = session.encrypt_and_ratchet("Directive: Move to Sector 7")

    print("Ciphertext 1:", c1)
    print("Ciphertext 2:", c2)
    assert c1["ciphertext_hex"] != c2["ciphertext_hex"], "Ratchet failed to alter keystream"
    print("Double Ratchet verified successfully!")

if __name__ == "__main__":
    main()
