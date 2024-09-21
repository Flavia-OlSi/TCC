let championImageJson = {};
const apiKey = "RGAPI-d727485e-e2cd-43b5-9fd0-e573e96d2f3e"; // Substitua com sua chave de API

// Função para buscar a versão mais recente e os dados dos campeões
async function getLatestDDragon() {
    try {
        const versionsResponse = await fetch("https://ddragon.leagueoflegends.com/api/versions.json");
        if (!versionsResponse.ok) throw new Error("Failed to fetch versions");

        const versions = await versionsResponse.json();
        const latest = versions[0];

        const ddragonResponse = await fetch(`https://ddragon.leagueoflegends.com/cdn/${latest}/data/en_US/champion.json`);
        if (!ddragonResponse.ok) throw new Error("Failed to fetch champion data");

        const champions = await ddragonResponse.json();
        championImageJson = champions.data; // Armazena os dados dos campeões
        return championImageJson;
    } catch (error) {
        console.error("Error fetching data:", error);
    }
}

// Função para buscar os jogos em destaque da API da Riot
async function getFeaturedGames() {
    try {
        const response = await fetch(`https://br1.api.riotgames.com/lol/spectator/v5/featured-games?api_key=${apiKey}`);
        if (!response.ok) throw new Error("Failed to fetch featured games");

        const gamesData = await response.json();
        return gamesData;
    } catch (error) {
        console.error("Error fetching featured games:", error);
        return null;
    }
}

// Função para mapear o championId para o nome e imagem do campeão
async function getChampionByKey(key) {
    if (!championImageJson || Object.keys(championImageJson).length === 0) {
        await getLatestDDragon();
    }

    for (let championName in championImageJson) {
        if (championImageJson[championName]["key"] === key.toString()) {
            return championImageJson[championName];
        }
    }
    return null;
}

// Função auxiliar para gerar o HTML dos jogadores por time
const createTeamHtml = async (team, className) => {
    return Promise.all(
        team.map(async (participant) => {
            const time = participant.teamId;
            const championId = participant.championId;
            const riotId = participant.riotId; // Nome do invocador
            const championInfo = await getChampionByKey(championId);

            if (championInfo && time === 100) {
                return `
                    <div class="card-jogador-${className}">
                        <p>${riotId}</p>
                        <img src="https://lolcdn.darkintaqt.com/cdn/champion/${championInfo.key}/tile" alt="${championInfo.name}" />
                    </div>
                `;
            } 
            else if (championInfo && time === 200) {
                return `
                    <div class="card-jogador-${className}">
                        <img src="https://lolcdn.darkintaqt.com/cdn/champion/${championInfo.key}/tile" alt="${championInfo.name}" />
                        <p>${riotId}</p>
                    </div>
                `;
            } else {
                return `
                    <div class="card-jogador-${className}">
                        <p>${riotId}</p>
                        <p>Champion not found</p>
                    </div>
                `;
            }
        })
    );
};

// Função para substituir os championIds com nome, imagem e riotId para todas as partidas
async function replaceChampionIdsWithNamesForGames() {
    const featuredGames = await getFeaturedGames();
    if (!featuredGames) return;

    const gameList = featuredGames.gameList;

    let allGamesHtml = ""; // Armazena o HTML de todas as partidas

    // Iterar sobre cada partida
    for (let i = 0; i < gameList.length; i++) {
        const game = gameList[i];
        const gameParticipants = game.participants;

        // Separar jogadores por time (Azul: teamId = 100, Vermelho: teamId = 200)
        const blueTeam = gameParticipants.filter(participant => participant.teamId === 100);
        const redTeam = gameParticipants.filter(participant => participant.teamId === 200);

        // Gerar HTML para cada time
        const blueTeamHtml = (await createTeamHtml(blueTeam, "azul")).join("");
        const redTeamHtml = (await createTeamHtml(redTeam, "vermelho")).join("");

        // Adicionar a partida ao HTML geral
        allGamesHtml += `
            <div class="card partida-card">
                <div class="card-titulo">
                    <p>Ranqueada Solo/Duo</p>
                </div>
                <div class="card-titulo">
                    <p>(20:40)</p>
                </div>
                <div class="card-jogadores">
                    <div id="blue-team-${i}" class="team">
                        <h4 style ="padding-left: 5vh">Time Azul</h4>
                        ${blueTeamHtml}
                    </div>
                    <div id="red-team-${i}" class="team">
                        <h4 style ="padding-left: 2vh">Time Vermelho</h4>
                        ${redTeamHtml}
                    </div>                           
                </div>
                <div class="card-previsao">
                    <h4>Previsão de Vitória:</h4>
                    <p>Time Azul</p>
                </div>
            </div>
        `;
    }

    // Exibir todas as partidas no DOM
    document.getElementById("featured-games").innerHTML = allGamesHtml;
}

// Função principal
async function main() {
    await getLatestDDragon(); // Carrega os dados dos campeões do DDragon
    await replaceChampionIdsWithNamesForGames(); // Substitui os IDs pelos nomes, imagens e riotId para todas as partidas
}

main();
