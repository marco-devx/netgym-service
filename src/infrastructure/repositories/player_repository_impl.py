from typing import List, Optional

from sqlalchemy import select
from sqlalchemy.dialects.postgresql import insert

from src.domain.entities.player import Player
from src.domain.ports.repositories import PlayerRepository
from src.infrastructure.config.databases.db_config import SessionLocal
from src.infrastructure.models import PlayerModel
from src.shared.exceptions import DatabaseException
from src.infrastructure.exceptions import handle_db_exception


class PlayerRepositoryAdapter(PlayerRepository):
    def save(self, player_override: Player) -> Player:
        try:
            with SessionLocal() as session:
                stmt = insert(PlayerModel).values(
                    name=player_override.name,
                    position=player_override.position,
                    games=player_override.games,
                    at_bats=player_override.at_bats,
                    runs=player_override.runs,
                    hits=player_override.hits,
                    doubles=player_override.doubles,
                    triples=player_override.triples,
                    homeruns=player_override.homeruns,
                    rbi=player_override.rbi,
                    walks=player_override.walks,
                    strikeouts=player_override.strikeouts,
                    stolen_bases=player_override.stolen_bases,
                    caught_stealing=player_override.caught_stealing,
                    average=player_override.average,
                    obp=player_override.obp,
                    slg=player_override.slg,
                    ops=player_override.ops
                )
                
                # Update all fields on conflict
                stmt = stmt.on_conflict_do_update(
                    index_elements=['name'],
                    set_={
                        c.name: c for c in stmt.excluded if c.name != 'created_at'
                    }
                )
                
                session.execute(stmt)
                session.commit()
                
                # Fetch the saved object to return it
                return self.get_override_by_name(player_override.name)
                
        except Exception as e:
            handle_db_exception(e, "Error saving player override")

    def get_all_overrides(self) -> List[Player]:
        """Get all player overrides."""
        try:
            with SessionLocal() as session:
                stmt = select(PlayerModel)
                result = session.execute(stmt).scalars().all()
                
                return [self._to_entity(model) for model in result]
        except Exception as e:
            handle_db_exception(e, "Error fetching player overrides")

    def get_override_by_name(self, name: str) -> Optional[Player]:
        """Get a specific player override by name."""
        try:
            with SessionLocal() as session:
                stmt = select(PlayerModel).where(PlayerModel.name == name)
                model = session.execute(stmt).scalar_one_or_none()
                
                if model:
                    return self._to_entity(model)
                return None
        except Exception as e:
            handle_db_exception(e, f"Error fetching player override for {name}")

    def _to_entity(self, model: PlayerModel) -> Player:
        """Convert model to entity."""
        return Player(
            name=model.name,
            position=model.position,
            games=model.games,
            at_bats=model.at_bats,
            runs=model.runs,
            hits=model.hits,
            doubles=model.doubles,
            triples=model.triples,
            homeruns=model.homeruns,
            rbi=model.rbi,
            walks=model.walks,
            strikeouts=model.strikeouts,
            stolen_bases=model.stolen_bases,
            caught_stealing=model.caught_stealing,
            average=model.average,
            obp=model.obp,
            slg=model.slg,
            ops=model.ops
        )
