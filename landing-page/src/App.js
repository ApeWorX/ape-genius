import "./styles.css";
import { useCallback } from "react";
import Particles from "react-particles";
import { loadSlim } from "tsparticles-slim"; // if you are going to use `loadSlim`, install the "tsparticles-slim" package too.

const scrollTo = (section) => {
  document.getElementById(section).scrollIntoView({
    behavior: "smooth"
  });
};

export default function App() {
  const particlesInit = useCallback(async (engine) => {
    console.log(engine);
    // you can initiate the tsParticles instance (engine) here, adding custom shapes or presets
    // this loads the tsparticles package bundle, it's the easiest method for getting everything ready
    // starting from v2 you can add only the features you need reducing the bundle size
    //await loadFull(engine);
    await loadSlim(engine);
  }, []);

  const particlesLoaded = useCallback(async (container) => {
    await console.log(container);
  }, []);

  return (
    <div className="app">
      <Particles
        id="tsparticles"
        init={particlesInit}
        loaded={particlesLoaded}
        options={{
          autoPlay: true,
          defaultThemes: {},
          delay: 0,
          detectRetina: true,
          duration: 0,
          interactivity: {
            detectsOn: "window",
            events: {
              onDiv: {
                selectors: [],
                enable: false,
                mode: [],
                type: "circle"
              },
              onHover: {
                enable: true,
                mode: "grab"
              },
              resize: {
                delay: 0.5,
                enable: true
              }
            },
            modes: {
              trail: {
                delay: 1,
                pauseOnStop: false,
                quantity: 1
              },
              attract: {
                distance: 200,
                duration: 0.4,
                easing: "ease-out-quad",
                factor: 1,
                maxSpeed: 50,
                speed: 1
              },
              bounce: {
                distance: 200
              },
              bubble: {
                distance: 400,
                duration: 2,
                mix: false,
                opacity: 0.8,
                size: 40,
                divs: {
                  distance: 200,
                  duration: 0.4,
                  mix: false,
                  selectors: []
                }
              },
              connect: {
                distance: 80,
                links: {
                  opacity: 0.5
                },
                radius: 60
              },
              grab: {
                distance: 400,
                links: {
                  blink: false,
                  consent: false,
                  opacity: 1
                }
              },
              push: {
                default: true,
                groups: [],
                quantity: 4
              },
              remove: {
                quantity: 2
              },
              repulse: {
                distance: 200,
                duration: 0.4,
                factor: 100,
                speed: 1,
                maxSpeed: 50,
                easing: "ease-out-quad",
                divs: {
                  distance: 200,
                  duration: 0.4,
                  factor: 100,
                  speed: 1,
                  maxSpeed: 50,
                  easing: "ease-out-quad",
                  selectors: []
                }
              },
              slow: {
                factor: 3,
                radius: 200
              },
              light: {
                area: {
                  gradient: {
                    start: {
                      value: "#ffffff"
                    },
                    stop: {
                      value: "#000000"
                    }
                  },
                  radius: 1000
                },
                shadow: {
                  color: {
                    value: "#000000"
                  },
                  length: 2000
                }
              }
            }
          },
          manualParticles: [],
          particles: {
            bounce: {
              horizontal: {
                random: {
                  enable: false,
                  minimumValue: 0.1
                },
                value: 1
              },
              vertical: {
                random: {
                  enable: false,
                  minimumValue: 0.1
                },
                value: 1
              }
            },
            collisions: {
              absorb: {
                speed: 2
              },
              bounce: {
                horizontal: {
                  random: {
                    enable: false,
                    minimumValue: 0.1
                  },
                  value: 1
                },
                vertical: {
                  random: {
                    enable: false,
                    minimumValue: 0.1
                  },
                  value: 1
                }
              },
              enable: false,
              maxSpeed: 50,
              mode: "bounce",
              overlap: {
                enable: true,
                retries: 0
              }
            },
            color: {
              value: "#ffffff",
              animation: {
                h: {
                  count: 0,
                  enable: false,
                  offset: 0,
                  speed: 1,
                  delay: 0,
                  decay: 0,
                  sync: true
                },
                s: {
                  count: 0,
                  enable: false,
                  offset: 0,
                  speed: 1,
                  delay: 0,
                  decay: 0,
                  sync: true
                },
                l: {
                  count: 0,
                  enable: false,
                  offset: 0,
                  speed: 1,
                  delay: 0,
                  decay: 0,
                  sync: true
                }
              }
            },
            groups: {},
            move: {
              angle: {
                offset: 0,
                value: 90
              },
              attract: {
                distance: 200,
                enable: false,
                rotate: {
                  x: 600,
                  y: 1200
                }
              },
              center: {
                x: 50,
                y: 50,
                mode: "percent",
                radius: 0
              },
              decay: 0,
              distance: {},
              direction: "none",
              drift: 0,
              enable: true,
              gravity: {
                acceleration: 9.81,
                enable: false,
                inverse: false,
                maxSpeed: 50
              },
              path: {
                clamp: true,
                delay: {
                  random: {
                    enable: false,
                    minimumValue: 0
                  },
                  value: 0
                },
                enable: false,
                options: {}
              },
              outModes: {
                default: "out",
                bottom: "out",
                left: "out",
                right: "out",
                top: "out"
              },
              random: false,
              // size: false,
              speed: 2,
              spin: {
                acceleration: 0,
                enable: false
              },
              straight: false,
              trail: {
                enable: false,
                length: 10,
                fill: {}
              },
              vibrate: false,
              warp: false
            },
            number: {
              density: {
                enable: true,
                width: 1920,
                height: 1080
              },
              limit: 0,
              value: 100
            },
            opacity: {
              random: {
                enable: true,
                minimumValue: 0.1
              },
              value: {
                min: 0.1,
                max: 0.5
              },
              animation: {
                count: 0,
                enable: true,
                speed: 3,
                decay: 0,
                delay: 0,
                sync: false,
                mode: "auto",
                startValue: "random",
                destroy: "none",
                minimumValue: 0.1
              }
            },
            reduceDuplicates: false,
            shadow: {
              blur: 0,
              color: {
                value: "#000"
              },
              enable: false,
              offset: {
                x: 0,
                y: 0
              }
            },
            shape: {
              close: true,
              fill: true,
              options: {},
              type: "circle"
            },
            size: {
              random: {
                enable: true,
                minimumValue: 1
              },
              value: {
                min: 0.1,
                max: 10
              },
              animation: {
                count: 0,
                enable: true,
                speed: 20,
                decay: 0,
                delay: 0,
                sync: false,
                mode: "auto",
                startValue: "random",
                destroy: "none",
                minimumValue: 0.1
              }
            },
            stroke: {
              width: 0
            },
            zIndex: {
              random: {
                enable: false,
                minimumValue: 0
              },
              value: 0,
              opacityRate: 1,
              sizeRate: 1,
              velocityRate: 1
            },
            destroy: {
              bounds: {},
              mode: "none",
              split: {
                count: 1,
                factor: {
                  random: {
                    enable: false,
                    minimumValue: 0
                  },
                  value: 3
                },
                rate: {
                  random: {
                    enable: false,
                    minimumValue: 0
                  },
                  value: {
                    min: 4,
                    max: 9
                  }
                },
                sizeOffset: true,
                particles: {}
              }
            },
            roll: {
              darken: {
                enable: false,
                value: 0
              },
              enable: false,
              enlighten: {
                enable: false,
                value: 0
              },
              mode: "vertical",
              speed: 25
            },
            tilt: {
              random: {
                enable: false,
                minimumValue: 0
              },
              value: 0,
              animation: {
                enable: false,
                speed: 0,
                decay: 0,
                sync: false
              },
              direction: "clockwise",
              enable: false
            },
            twinkle: {
              lines: {
                enable: false,
                frequency: 0.05,
                opacity: 1
              },
              particles: {
                enable: false,
                frequency: 0.05,
                opacity: 1
              }
            },
            wobble: {
              distance: 5,
              enable: false,
              speed: {
                angle: 50,
                move: 10
              }
            },
            life: {
              count: 0,
              delay: {
                random: {
                  enable: false,
                  minimumValue: 0
                },
                value: 0,
                sync: false
              },
              duration: {
                random: {
                  enable: false,
                  minimumValue: 0.0001
                },
                value: 0,
                sync: false
              }
            },
            rotate: {
              random: {
                enable: false,
                minimumValue: 0
              },
              value: 0,
              animation: {
                enable: false,
                speed: 0,
                decay: 0,
                sync: false
              },
              direction: "clockwise",
              path: false
            },
            orbit: {
              animation: {
                count: 0,
                enable: false,
                speed: 1,
                decay: 0,
                delay: 0,
                sync: false
              },
              enable: false,
              opacity: 1,
              rotation: {
                random: {
                  enable: false,
                  minimumValue: 0
                },
                value: 45
              },
              width: 1
            },
            links: {
              blink: false,
              color: {
                value: "#ffffff"
              },
              consent: false,
              distance: 150,
              enable: true,
              frequency: 1,
              opacity: 0.4,
              shadow: {
                blur: 5,
                color: {
                  value: "#000"
                },
                enable: false
              },
              triangles: {
                enable: false,
                frequency: 1
              },
              width: 1,
              warp: false
            },
            repulse: {
              random: {
                enable: false,
                minimumValue: 0
              },
              value: 0,
              enabled: false,
              distance: 1,
              duration: 1,
              factor: 1,
              speed: 1
            }
          },
          pauseOnBlur: true,
          pauseOnOutsideViewport: true,
          responsive: [],
          smooth: false,
          style: {},
          themes: [],
          zLayers: 100,
          motion: {
            disable: false,
            reduce: {
              factor: 4,
              value: true
            }
          }
        }}
      />
      <div className="app-inner">
        <div className="section" id="section-1">
          <div className="half-width">
            <img className="logo" src="ape-logo.png" width="256" />
            <h1>Ape Genius</h1>
            <h2>The smartest ape in the jungle</h2>
            <div className="navigator">
              <a onClick={() => scrollTo("")}>About</a>
              <a onClick={() => scrollTo("section-3")}>Examples</a>
              <a onClick={() => scrollTo("section-4")}>Follow</a>
              <a target="_blank" href="https://github.com/ApeWorX/ape-genius">Code</a>
              <a target="_blank" href="https://apeworx.io/">ApeWorX</a>
            </div>

            <button
              className="next-section"
              onClick={() => scrollTo("section-2")}
            >
              About
            </button>
          </div>
        </div>
        <div className="section" id="section-2">
          <h2>All ApeWorX knowledge</h2>
          <h2>at your fingertips</h2>
          <ul>
            <li>
              <h3>Accurate</h3>Search and compile deterministic answers using
              knowledge across all ApeWorX docs. The bot will always tell the
              sources used to answer you.
            </li>
            <li>
              <h3>Smart</h3>Always up-to-date with the latest GPT model, the
              entire <a href="https://docs.apeworx.io/">ape docs</a> are added
              to your requests. Can answer in many languages.
            </li>
            <li>
              <h3>Improves Documentation</h3>As we receive feedback from wrong
              answers we improve our docs, which improve answers.
            </li>
            <li>
              <h3>Open Source</h3>Easily setup and run the bot with your own
              knowledge base by{" "}
              <a href="https://github.com/ApeWorX/ape-genius">forking</a> our
              code.
            </li>
          </ul>
          <button
            className="next-section"
            onClick={() => scrollTo("section-3")}
          >
            Examples
          </button>
        </div>
        <div className="section" id="section-3">
          <h1>Examples Showcase</h1>
          <ul>
            <li>
              <h3>Developing Scripts</h3>
              INPUT:
              <p>a script that transfers DAI from one wallet to another</p>
              OUTPUT:
              <p>
                <pre>{`The following script demonstrates how to transfer DAI (an ERC-20 token) from one wallet to another using the Ape Framework. This script assumes you have the DAI contract address and the ABI for the DAI token, and that you have two accounts set up in Ape with the aliases sender_alias and receiver_alias.

Please replace DAI_CONTRACT_ADDRESS, SENDER_ALIAS, and RECEIVER_ALIAS with your actual DAI contract address and account aliases. Also, ensure you have the necessary DAI balance in the sender's account and that the sender has enough ETH to pay for gas.

from ape import accounts, Contract, networks

# Replace these variables with your actual values
DAI_CONTRACT_ADDRESS = "0x6B175474E89094C44Da98b954EedeAC495271d0F"  # Example DAI address on Ethereum mainnet
SENDER_ALIAS = "sender_alias"
RECEIVER_ALIAS = "receiver_alias"
AMOUNT_DAI_TO_SEND = 10  # Amount of DAI to send

# Load the sender and receiver accounts using their aliases
sender = accounts.load(SENDER_ALIAS)
receiver = accounts.load(RECEIVER_ALIAS)

# Connect to the Ethereum mainnet (or another network where your DAI tokens are)
with networks.parse_network_choice("ethereum:mainnet:infura") as provider:
    # Load the DAI contract
    dai_contract = Contract(DAI_CONTRACT_ADDRESS)

    # Check the sender's DAI balance
    sender_dai_balance = dai_contract.balanceOf(sender)
    print(f"Sender's DAI balance: {sender_dai_balance}")

    # Ensure the sender has enough DAI to send
    if sender_dai_balance < AMOUNT_DAI_TO_SEND:
        raise ValueError("Sender does not have enough DAI to send.")

    # Calculate the amount to send in the smallest unit (wei for Ethereum)
    amount_to_send_wei = provider.network.ecosystem.encode_scale(AMOUNT_DAI_TO_SEND)

    # Transfer DAI from the sender to the receiver
    transfer_txn = dai_contract.transfer(receiver, amount_to_send_wei, sender=sender)

    # Wait for the transaction to be confirmed
    receipt = transfer_txn.wait_for_confirmation()

    # Check the transaction status
    if receipt.status == 1:
        print(f"Successfully transferred {AMOUNT_DAI_TO_SEND} DAI to {receiver}.")
    else:
        print("DAI transfer failed.")

This script is a simple example and does not include error handling or advanced features like gas estimation. Make sure to test the script on a testnet before using it on the mainnet to avoid losing funds due to mistakes.

Note: This answer is creative and goes beyond the source files provided, as it includes a practical example of how to use the Ape Framework to transfer ERC-20 tokens. The actual contract address and ABI for DAI, as well as the account aliases, should be provided by the user.`}</pre>
              </p>
            </li>
            <li>
              <h3>Questions & Answers</h3>
              INPUT:
              <p>how to create and fund a new account in ethereum using ape?</p>
              OUTPUT:
              <p>
                <pre>
                  To create and fund a new account in Ethereum using Ape, you
                  can follow these steps:
                  <br />
                  <br />
                  1. Create a New Account: Use the ape accounts generate command
                  to create a new account. You will be prompted to enter a
                  passphrase to secure the account.
                  <br />
                  <br />
                  ape accounts generate my_new_account
                  <br />
                  <br />
                  2. Fund the Account: To fund the account, you will need to
                  send Ether to the new account's address. This can be done from
                  a faucet if you are on a testnet, or by transferring Ether
                  from an existing account if you are on the mainnet.
                  <br />
                  <br />
                  If you are on a testnet like Rinkeby, you can use a faucet to
                  get test Ether. Go to the faucet website, enter your new
                  account's address, and request funds.
                  <br />
                  <br />
                  If you are on the mainnet or a testnet without a faucet, you
                  can transfer Ether to your new account's address from an
                  existing account using a wallet or exchange.
                  <br />
                  <br />
                  3. Check Account Balance: After funding the account, you can
                  check the balance using the ape accounts list command to
                  ensure the funds have been received.
                  <br />
                  <br />
                  ape accounts list
                  <br />
                  <br />
                  This will list all your accounts along with their balances.
                  <br />
                  <br />
                  Source: The information is based on the ape accounts generate
                  and ape accounts list commands as described in the
                  ./docs\docs-readme.md document.
                </pre>
              </p>
            </li>
            <li>
              <h3>Social Media</h3>
              INPUT:
              <p>
                a twitter thread explaining all of ape features and why are they
                useful, make a catchy clickbait first post then one post per
                useful thing, last post should be a CTA to apeworx.io
              </p>
              OUTPUT:
              <p>
                <pre>
                  🚀 Introducing Ape Framework: The Ultimate Web3 Dev Swiss Army
                  Knife!
                  <br />
                  <br />
                  Are you ready to revolutionize your smart contract
                  development? Look no further than Ape Framework! Dive into
                  this thread to discover how Ape supercharges your Web3
                  workflow! 🧵👇
                  <br />
                  <br />
                  1️⃣ Seamless Smart Contract Interaction 🤝 Ape Framework allows
                  you to compile, test, and interact with smart contracts
                  effortlessly. Say goodbye to the hassle of switching tools
                  mid-development! 🛠️💻
                  <br />
                  <br />
                  2️⃣ Modular Plugin System 🧩 With Ape's modular plugin system,
                  you're not limited to one language or blockchain. Enjoy the
                  freedom to work with multiple contract languages and chains!
                  Expand your horizons! 🌐🔗
                  <br />
                  <br />
                  3️⃣ Built for Developers, by Developers 👨‍💻👩‍💻 Crafted by the
                  experts at ApeWorX LTD, Ape Framework is designed with the
                  developer's needs in mind. Join a community that speaks your
                  language! 🤝🌟
                  <br />
                  <br />
                  4️⃣ CLI and Python SDK: Best of Both Worlds 🌍 Whether you love
                  the command line or live in Python scripts, Ape has you
                  covered. Execute commands or write scripts with ease –
                  flexibility at its finest! 🐍💻
                  <br />
                  <br />
                  5️⃣ Account Management Simplified 🔐 Manage your Web3 accounts
                  with ease. Import, generate, and list accounts right from the
                  command line. Secure transactions are just a command away!
                  🔑🔒
                  <br />
                  <br />
                  6️⃣ Effortless Project Management 📁 Ape understands your
                  project structure, making it a breeze to compile contracts,
                  run scripts, and manage dependencies. Focus on building, not
                  configuring! 🏗️📈
                  <br />
                  <br />
                  7️⃣ Testing Made Easy 🧪 With Ape, testing your smart contracts
                  is a walk in the park. Use pytest fixtures and enjoy built-in
                  test isolation. Deliver robust code with confidence! ✅🚀
                  <br />
                  <br />
                  8️⃣ Interactive Console 🎮 Jump into Ape's interactive console
                  for real-time contract interaction. Debug and develop in an
                  environment that's as dynamic as your ideas! 🖥️💡
                  <br />
                  <br />
                  9️⃣ Comprehensive Documentation and Support 📚 Never feel lost
                  with Ape's extensive documentation and academic platform.
                  Master Ape Framework with tutorials and challenges! 🎓📖
                  <br />
                  <br />
                  🔟 Cross-Platform Compatibility 🖥️🍏🪟 Ape works on Linux,
                  macOS, and even Windows (with WSL). Develop on the platform
                  you love without any barriers! 🚧🔄
                  <br />
                  <br />
                  Ready to transform your smart contract development experience?
                  Join the Ape revolution now! 🚀
                  <br />
                  <br />
                  Discover more and become a part of the Ape community at
                  ApeWorX.io. Let's build the future of Web3 together! 🛠️🔗🌍
                  <br />
                  <br />
                  #Web3 #SmartContracts #BlockchainDevelopment #ApeFramework
                  #BuildTheFuture
                </pre>
              </p>
            </li>
          </ul>
          <button
            className="next-section"
            onClick={() => scrollTo("section-4")}
          >
            Follow Updates
          </button>
        </div>
        <div className="section" id="section-4">
          <h1>Follow Our Updates</h1>
          <h3>
            Today we host and serve Ape Genius
            <br />
            only for ApeWorX partners
          </h3>
          <h3>
            Follow our Telegram announcements group
            <br />
            and get preview access when available
          </h3>
          <div className="submit">
            {/* <input /> */}
            <a target="_blank" href="https://t.me/apegenius" className="submit-btn">📣 Follow Ape Genius Announcements</a>
            <a target="_blank" href="https://twitter.com/ApeFramework" className="submit-btn">🐦 Follow Ape on Twitter</a>
            <a target="_blank" href="https://github.com/ApeWorX/apegenius" className="submit-btn">🍴 Fork Ape Genius Source Code</a>
          </div>
          {/* <ul>
            <li>
              <b>Today</b> - Partners that pay ape receive acess to the bot via
              Telegram for free for up to 10 requests per day.
            </li>
            <li>
              <b>Future</b> - We are studying ways to rollout this product for
              the public, if you are interested{" "}
              <a href="#">apply for preview access</a>.
            </li>
          </ul>
          <div>
            <input />
            <button>Apply</button>
          </div> */}
          <button
            className="next-section alt"
            onClick={() => scrollTo("section-1")}
          >
            Scroll to Top
          </button>
        </div>
      </div>
    </div>
  );
}
